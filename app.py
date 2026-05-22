import os

import numpy as np
import tensorflow as tf
from fastapi import FastAPI
from pydantic import BaseModel, Field


@tf.keras.utils.register_keras_serializable()
class CustomDenseLayer(tf.keras.layers.Layer):
    def __init__(self, units, activation=None, **kwargs):
        super().__init__(**kwargs)
        self.units = units
        self.activation = tf.keras.activations.get(activation)

    def build(self, input_shape):
        self.w = self.add_weight(
            shape=(input_shape[-1], self.units),
            initializer="random_normal",
            trainable=True,
            name="custom_weight",
        )
        self.b = self.add_weight(
            shape=(self.units,),
            initializer="zeros",
            trainable=True,
            name="custom_bias",
        )

    def call(self, inputs):
        output = tf.matmul(inputs, self.w) + self.b
        if self.activation is not None:
            output = self.activation(output)
        return output

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "units": self.units,
                "activation": tf.keras.activations.serialize(self.activation),
            }
        )
        return config


app = FastAPI(title="Risk Profile Model API")
model = tf.keras.models.load_model(
    "risk_profile_model.keras",
    custom_objects={"CustomDenseLayer": CustomDenseLayer},
)

FEATURE_MEAN = np.array(
    [
        0.4517512115616774,
        0.5359481639989531,
        0.2747191795214599,
        0.4751019024748894,
        679.5367264586861,
        0.48475,
        35.937,
        10.479874342843136,
        41.04625,
        14.70975,
    ],
    dtype=np.float32,
)
FEATURE_SCALE = np.array(
    [
        0.27280096375993285,
        0.25361946801694374,
        0.19722968395700197,
        0.24699884640255088,
        59.07589130646918,
        0.6886707758428381,
        17.22416996548745,
        4.332927775472363,
        13.353599175409602,
        8.686253791911698,
    ],
    dtype=np.float32,
)


class RiskProfileInput(BaseModel):
    age: float
    annual_income: float = Field(gt=0)
    credit_score: float
    loan_amount: float
    loan_duration_months: float
    interest_rate: float
    debt_to_income_ratio: float
    monthly_expenses: float
    savings_balance: float
    employment_stability_years: float
    previous_default_count: float


@app.get("/")
def root():
    return {"message": "Risk Profile Model API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(payload: RiskProfileInput):
    loan_to_income_ratio = payload.loan_amount / payload.annual_income
    expenses_to_income_ratio = payload.monthly_expenses / (payload.annual_income / 12)
    savings_to_income_ratio = payload.savings_balance / payload.annual_income

    features = np.array(
        [
            [
                loan_to_income_ratio,
                expenses_to_income_ratio,
                savings_to_income_ratio,
                payload.debt_to_income_ratio,
                payload.credit_score,
                payload.previous_default_count,
                payload.loan_duration_months,
                payload.interest_rate,
                payload.age,
                payload.employment_stability_years,
            ]
        ],
        dtype=np.float32,
    )
    features = (features - FEATURE_MEAN) / FEATURE_SCALE

    prediction = model.predict(features, verbose=0)
    probabilities = prediction[0].tolist()
    predicted_label = int(np.argmax(prediction, axis=1)[0])

    return {
        "risk_profile_label": predicted_label,
        "probabilities": probabilities,
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
