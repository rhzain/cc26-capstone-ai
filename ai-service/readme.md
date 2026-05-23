# CuanSelor AI Service

FastAPI service for the risk profile model.

## Railway setup

Deploy this service in the same Railway project/environment as the Express
backend, but do not generate a public domain for it. Express should be the only
public API gateway.

Set the same internal token on both services:

```env
INTERNAL_API_TOKEN=<shared-secret>
```

On the Express backend service, set:

```env
ML_SERVICE_URL=http://<fastapi-service-name>.railway.internal:8000
INTERNAL_API_TOKEN=<shared-secret>
```

The FastAPI `/predict` route rejects requests without `X-Internal-Token`, so
browser and public clients should call Express instead:

```txt
POST /api/ml/risk-profile
```
