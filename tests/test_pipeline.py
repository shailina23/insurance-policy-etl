from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
fact = pd.read_csv(ROOT/"data/output/fact_policy_analytics.csv")

assert fact["policy_id"].notna().all()
assert fact["customer_id"].notna().all()
assert (fact["premium"] >= 0).all()
assert (fact["paid_claim_amount"] >= 0).all()
assert fact["policy_id"].is_unique
print("All insurance pipeline checks passed.")
