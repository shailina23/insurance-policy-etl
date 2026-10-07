# Data contract

All input records in this repository are synthetic and created for a portfolio demonstration.

## Inputs and row grain

| File | Grain | Key fields |
| --- | --- | --- |
| `data/raw/customers.csv` | One row per customer | `customer_id` |
| `data/raw/policies.csv` | One row per policy | `policy_id`, `customer_id` |
| `data/raw/claims.csv` | One row per claim | `claim_id`, `policy_id` |

## Output: `fact_policy_analytics`

**Grain:** one row per policy.

The output combines policy attributes, customer state/segment, and claim aggregates. `claim_count` and `total_claim_amount` include all claim statuses. `paid_claim_amount` includes only rows whose `claim_status` is `Paid`.

## KPI definition

```text
loss_ratio_proxy = paid_claim_amount / premium
```

This is a simplified portfolio-demo proxy, not an actuarial or regulatory measure. The example assumes positive policy premiums; the current pipeline does not define special handling for a zero premium. Confirm status treatment, premium definitions, currency, and reporting period with business owners in any real project.

## Implemented checks

The current script in `tests/test_pipeline.py` checks the generated policy fact for non-null policy/customer IDs, non-negative premium and paid claim amount, and unique policy IDs. Run the pipeline first to generate the file it reads.

## Further checks to add

The following are desired contract rules but are not yet fully enforced by the pipeline:

- Validate required columns and parseable dates in every source file.
- Check source key uniqueness and foreign-key references before joining.
- Reject or quarantine negative premiums and claim amounts.
- Define zero-premium behavior for the KPI.
- Report unmatched policy/customer and claim/policy keys.
- Make output generation deterministic and add a separate test fixture for invalid input.
