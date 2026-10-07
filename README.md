# Insurance Policy and Claims ETL

A small Python and pandas portfolio project that combines synthetic customer, policy, and claims extracts into a policy-level table and a product/state KPI summary.

> **Portfolio lab:** all records and business rules are fictional. This is not client work, an insurance system, or a production-ready pipeline.

## Scenario and outputs

The example insurer receives three CSV extracts. The pipeline standardizes selected text fields, parses dates, aggregates claims by policy, joins customer and policy data, and writes:

- `data/output/fact_policy_analytics.csv` — one row per policy.
- `data/output/insurance_kpi_summary.csv` — one row per product and state.

The `loss_ratio_proxy` is paid claim amount divided by premium. Only claims with `claim_status` equal to `Paid` contribute to the numerator; all claims contribute to `claim_count` and `total_claim_amount`. This is a demo KPI definition, not an actuarial loss ratio.

## Run locally

Requires Python 3.10 or later.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install -r requirements.txt
python src/pipeline.py
```

The pipeline creates `data/output/` and prints the number of policy records and KPI rows. The test script reads the generated policy fact, so run the pipeline first.

## Current checks and limitations

The included test script checks that generated policy IDs and customer IDs are present, premiums and paid claim amounts are non-negative, and policy IDs are unique. It is a small demonstration check, not a complete validation framework.

The current pipeline does not yet enforce every expectation in the data contract. For example, it does not explicitly validate required input columns, duplicate source claim IDs, negative raw claim amounts, zero premiums, or unmatched customer references before transformation. Add those checks before describing the project as enforcing the full contract. The project also has no scheduler, warehouse connection, or deployed cloud component.

## Repository layout

```text
data/raw/       Synthetic customer, policy, and claims CSVs
src/            Transformation pipeline
docs/           Architecture and data contract
```

See [`docs/architecture.md`](docs/architecture.md) and [`docs/data_contract.md`](docs/data_contract.md) for the workflow and assumptions.
