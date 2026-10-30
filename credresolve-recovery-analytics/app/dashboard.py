from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/"outputs"
st.set_page_config(page_title="CredResolve Recovery Intelligence",layout="wide")
st.title("CredResolve | Recovery Intelligence")
st.caption("Independent analysis. Validate definitions before business decisions.")
mp=OUT/"monthly_recovery_metrics.csv"; qp=OUT/"data_quality_report.csv"
if not mp.exists():
    st.warning("Run python src/run_pipeline.py first."); st.stop()
m=pd.read_csv(mp); q=pd.read_csv(qp)
c1,c2,c3=st.columns(3)
c1.metric("Months",m.month.nunique() if len(m) else 0)
c2.metric("Successful collections",f"₹{m.successful_payment_amount.sum():,.0f}" if len(m) else "₹0")
c3.metric("Distinct monthly account count sum",f"{m.accounts_paid.sum():,}" if len(m) else "0")
if len(m):
    st.plotly_chart(px.line(m,x="month",y="successful_payment_amount",markers=True),use_container_width=True)
    st.dataframe(m,use_container_width=True)
st.subheader("Data quality")
st.metric("Source tables",len(q)); st.metric("Exact duplicate rows",int(q.exact_duplicate_rows.sum()))
st.metric("Missing cells",int(q.missing_cells.sum())); st.dataframe(q,use_container_width=True)
st.info("This is successful payment amount, not a validated recovery rate. A defensible denominator and attribution policy are still required.")
