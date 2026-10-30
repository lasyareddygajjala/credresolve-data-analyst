from pathlib import Path
import zipfile
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
ZIP=ROOT/"data/raw/credresolve_collections_dataset.zip"
SRC=ROOT/"data/source"
OUT=ROOT/"outputs"
SUCCESS={"SUCCESS","SUCCESSFUL","SETTLED","COMPLETED","PAID"}

def load_tables():
    SRC.mkdir(parents=True,exist_ok=True)
    if not list(SRC.glob("*.csv")):
        with zipfile.ZipFile(ZIP) as z: z.extractall(SRC)
    return {p.stem:pd.read_csv(p,low_memory=False) for p in SRC.glob("*.csv") if p.name!="data_dictionary.csv"}

def profile(tables):
    out=[]
    for name,df in tables.items():
        out.append({"table":name,"rows_raw":len(df),"columns":len(df.columns),
          "exact_duplicate_rows":int(df.duplicated().sum()),
          "rows_after_exact_dedup":len(df.drop_duplicates()),
          "missing_cells":int(df.isna().sum().sum()),
          "missing_pct":round(df.isna().sum().sum()/max(df.size,1)*100,3)})
    return pd.DataFrame(out).sort_values("table")

def clean(tables):
    result={}
    for name,df in tables.items():
        x=df.drop_duplicates().copy()
        for c in x.columns:
            if c.endswith("_at") or c.endswith("_date"):
                x[c]=pd.to_datetime(x[c],errors="coerce",utc=True)
        result[name]=x
    return result

def golden_payments(t):
    p=t["payments"].copy()
    p["event_at"]=pd.to_datetime(p["event_at"],errors="coerce",utc=True)
    p["amount"]=pd.to_numeric(p["amount"],errors="coerce")
    p["status_norm"]=p["payment_status"].astype(str).str.upper().str.strip()
    p["is_successful"]=p["status_norm"].isin(SUCCESS)
    ref=p["payment_reference"].notna()
    p["dedupe_key"]=np.where(ref,p["account_id"].astype(str)+"|"+p["payment_reference"].astype(str),p["payment_id"].astype(str))
    p=p.sort_values("event_at",na_position="first").drop_duplicates("dedupe_key",keep="last")
    ac=t.get("accounts",pd.DataFrame())
    cols=[c for c in ["account_id","principal_amount","outstanding_amount","dpd","risk_segment","loan_type","status","timezone"] if c in ac.columns]
    if cols: p=p.merge(ac[cols].drop_duplicates("account_id"),on="account_id",how="left")
    return p

def monthly_metrics(p):
    x=p[p["is_successful"] & p["amount"].gt(0) & p["event_at"].notna()].copy()
    x["month"]=x["event_at"].dt.tz_convert(None).dt.to_period("M").astype(str)
    return x.groupby("month",as_index=False).agg(successful_payment_amount=("amount","sum"),
      successful_payment_count=("payment_id","nunique"),accounts_paid=("account_id","nunique")).sort_values("month")

def run():
    OUT.mkdir(exist_ok=True)
    raw=load_tables(); q=profile(raw); t=clean(raw)
    gp=golden_payments(t); mm=monthly_metrics(gp)
    q.to_csv(OUT/"data_quality_report.csv",index=False)
    gp.to_csv(OUT/"golden_payments.csv",index=False)
    mm.to_csv(OUT/"monthly_recovery_metrics.csv",index=False)
    pd.DataFrame([{"table":k,"rows":len(v),"columns":len(v.columns)} for k,v in raw.items()]).to_csv(OUT/"source_inventory.csv",index=False)
    raw["payments"]["payment_status"].value_counts(dropna=False).rename_axis("payment_status").reset_index(name="rows").to_csv(OUT/"payment_status_audit.csv",index=False)
    print(f"Loaded {len(raw)} tables. Raw payment rows={len(raw['payments'])}; golden payment rows={len(gp)}")
    print(f"Outputs: {OUT}")
    return q,gp,mm

if __name__=="__main__": run()
