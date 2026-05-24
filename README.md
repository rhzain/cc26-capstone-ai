# Financial Profile Segmentation

This project segments consumer-facing financial self-assessment profiles using unsupervised clustering labels and a TensorFlow classifier for API inference.

## Scope

The system does not use `credit_score`. It does not create a default, imputed, or synthetic credit score.

The output is a financial profile segment based on similarity between user financial characteristics. It is not a probability of default, credit score, loan eligibility result, approval prediction, or official credit decision.

## API Input

The `/predict` endpoint accepts these user-facing inputs:

```text
age
annual_income
loan_amount
loan_duration_months
interest_rate
debt_to_income_ratio
monthly_expenses
savings_balance
employment_stability_years
previous_default_count
```

## Feature Engineering

The pipeline derives these ratios:

```text
loan_to_income_ratio = loan_amount / annual_income
expenses_to_income_ratio = monthly_expenses / (annual_income / 12)
savings_to_income_ratio = savings_balance / annual_income
```

## Final Model Features

Clustering and classification use these final features:

```text
loan_to_income_ratio
expenses_to_income_ratio
savings_to_income_ratio
debt_to_income_ratio
previous_default_count
loan_duration_months
interest_rate
age
employment_stability_years
```

## Interpretation

Clusters are interpreted post-hoc by comparing cluster centroids with the global feature averages.

Repayment Capacity:

```text
loan_to_income_ratio
expenses_to_income_ratio
debt_to_income_ratio
```

Financial Resilience:

```text
0.6 * savings_to_income_ratio
0.4 * employment_stability_years
```

Repayment capacity pressure is weighted to avoid making `debt_to_income_ratio` too dominant:

```text
0.4 * loan_to_income_ratio
0.4 * expenses_to_income_ratio
0.2 * debt_to_income_ratio
```

Financial Behavior:

```text
previous_default_count
interest_rate
```

Demographic Context:

```text
age
```

Profile names are neutral segment labels:

```text
Cluster 0 - Financially Stable
Cluster 1 - Moderate Financial Capacity
Cluster 2 - Financially Vulnerable
```

Cluster merupakan hasil segmentasi tanpa label (unsupervised learning) dan tidak merepresentasikan risiko gagal bayar aktual maupun keputusan kredit resmi.

## Cluster Analysis

K-Means selected `k=3` based on the best silhouette score among `k=3` to `k=5`.

Global feature averages:

| Feature | Global Average |
| --- | ---: |
| `loan_to_income_ratio` | 0.4501 |
| `expenses_to_income_ratio` | 0.5366 |
| `savings_to_income_ratio` | 0.2747 |
| `debt_to_income_ratio` | 0.4748 |
| `previous_default_count` | 0.4840 |
| `loan_duration_months` | 36.0768 |
| `interest_rate` | 10.4989 |
| `age` | 41.0138 |
| `employment_stability_years` | 14.7094 |

### Raw Cluster 0 -> Moderate Financial Capacity

This raw cluster is mapped to final label `1`.

Centroid:

| Feature | Centroid | Difference vs Global |
| --- | ---: | ---: |
| `loan_to_income_ratio` | 0.7654 | 0.3154 |
| `expenses_to_income_ratio` | 0.8634 | 0.3268 |
| `savings_to_income_ratio` | 0.4834 | 0.2087 |
| `debt_to_income_ratio` | 0.4909 | 0.0161 |
| `previous_default_count` | 0.5082 | 0.0242 |
| `loan_duration_months` | 36.5199 | 0.4431 |
| `interest_rate` | 10.4123 | -0.0866 |
| `age` | 40.7482 | -0.2656 |
| `employment_stability_years` | 15.6803 | 0.9709 |

Dominant characteristics:

- Higher loan-to-income and expenses-to-income ratios.
- Higher savings-to-income ratio.
- Stronger employment stability.
- Slightly lower interest rate exposure.

Dimension summary:

| Dimension | Score |
| --- | ---: |
| Repayment Capacity Pressure | 0.9939 |
| Financial Resilience | 0.6835 |
| Financial Behavior Pressure | 0.0075 |

Interpretation: this segment has high repayment pressure, but it is partly balanced by stronger savings and employment stability. Because the profile is mixed rather than clearly fragile, it is named `Moderate Financial Capacity`.

### Raw Cluster 1 -> Financially Vulnerable

This raw cluster is mapped to final label `2`.

Centroid:

| Feature | Centroid | Difference vs Global |
| --- | ---: | ---: |
| `loan_to_income_ratio` | 0.3819 | -0.0681 |
| `expenses_to_income_ratio` | 0.4769 | -0.0597 |
| `savings_to_income_ratio` | 0.2307 | -0.0440 |
| `debt_to_income_ratio` | 0.4854 | 0.0106 |
| `previous_default_count` | 0.4696 | -0.0144 |
| `loan_duration_months` | 37.0316 | 0.9548 |
| `interest_rate` | 14.3387 | 3.8398 |
| `age` | 40.1661 | -0.8477 |
| `employment_stability_years` | 13.6416 | -1.0678 |

Dominant characteristics:

- Lower savings-to-income ratio.
- Lower employment stability.
- Higher interest rate exposure.
- Slightly longer loan duration.

Dimension summary:

| Dimension | Score |
| --- | ---: |
| Repayment Capacity Pressure | -0.1862 |
| Financial Resilience | -0.1837 |
| Financial Behavior Pressure | 0.4327 |

Interpretation: this segment is not the highest in loan and expense ratios, but weaker resilience and higher interest exposure make it more vulnerable to financial pressure. It is named `Financially Vulnerable`.

### Raw Cluster 2 -> Financially Stable

This raw cluster is mapped to final label `0`.

Centroid:

| Feature | Centroid | Difference vs Global |
| --- | ---: | ---: |
| `loan_to_income_ratio` | 0.3882 | -0.0618 |
| `expenses_to_income_ratio` | 0.4617 | -0.0749 |
| `savings_to_income_ratio` | 0.2327 | -0.0420 |
| `debt_to_income_ratio` | 0.4578 | -0.0170 |
| `previous_default_count` | 0.4883 | 0.0043 |
| `loan_duration_months` | 34.9535 | -1.1233 |
| `interest_rate` | 6.7460 | -3.7529 |
| `age` | 41.9588 | 0.9450 |
| `employment_stability_years` | 15.3656 | 0.6562 |

Dominant characteristics:

- Lower loan-to-income and expenses-to-income ratios.
- Lower debt-to-income ratio.
- Stronger employment stability.
- Much lower interest rate exposure.

Dimension summary:

| Dimension | Score |
| --- | ---: |
| Repayment Capacity Pressure | -0.2230 |
| Financial Resilience | -0.0984 |
| Financial Behavior Pressure | -0.4300 |

Interpretation: this segment has lower repayment pressure, stronger employment stability, and much lower interest exposure. It is named `Financially Stable`.

Final mapping:

| Raw Cluster | Final Label | Profile Name |
| ---: | ---: | --- |
| 0 | 1 | Moderate Financial Capacity |
| 1 | 2 | Financially Vulnerable |
| 2 | 0 | Financially Stable |

Cluster distribution after interpretation:

| Final Label | Profile Name | Count |
| ---: | --- | ---: |
| 0 | Financially Stable | 2089 |
| 1 | Moderate Financial Capacity | 854 |
| 2 | Financially Vulnerable | 2057 |
