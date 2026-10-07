from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw"
OUT = ROOT / "data/output"
OUT.mkdir(exist_ok=True)

customers = pd.read_csv(RAW/"customers.csv")
policies = pd.read_csv(RAW/"policies.csv")
claims = pd.read_csv(RAW/"claims.csv")

# Standardize strings and dates
for df, cols in [
    (customers, ["customer_id","state","segment"]),
    (policies, ["policy_id","customer_id","product","status"]),
    (claims, ["claim_id","policy_id","claim_status"])
]:
    for c in cols:
        df[c] = df[c].astype(str).str.strip()

policies["start_date"] = pd.to_datetime(policies["start_date"])
claims["claim_date"] = pd.to_datetime(claims["claim_date"])

# Curated policy-level fact table
policy_claims = claims.groupby("policy_id", as_index=False).agg(
    claim_count=("claim_id","count"),
    total_claim_amount=("claim_amount","sum"),
    paid_claim_amount=("claim_amount", lambda s: s[claims.loc[s.index,"claim_status"].eq("Paid")].sum())
)

fact = policies.merge(customers, on="customer_id", how="left").merge(policy_claims, on="policy_id", how="left")
fact[["claim_count","total_claim_amount","paid_claim_amount"]] = fact[
    ["claim_count","total_claim_amount","paid_claim_amount"]
].fillna(0)

fact["loss_ratio_proxy"] = (fact["paid_claim_amount"] / fact["premium"]).round(4)
fact.to_csv(OUT/"fact_policy_analytics.csv", index=False)

# KPI summary for BI
summary = fact.groupby(["product","state"], as_index=False).agg(
    policies=("policy_id","count"),
    premium=("premium","sum"),
    paid_claims=("paid_claim_amount","sum")
)
summary["loss_ratio_proxy"] = (summary["paid_claims"]/summary["premium"]).round(4)
summary.to_csv(OUT/"insurance_kpi_summary.csv", index=False)

print("Pipeline complete.")
print(f"Policy records: {len(fact):,}")
print(f"KPI rows: {len(summary):,}")
