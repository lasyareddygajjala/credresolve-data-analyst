# CredResolve Recovery Analytics

A reproducible, auditable investigation of the reported 11% month-on-month recovery improvement. Built around the supplied synthetic 17-table collections dataset.

## Quick start

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/run_pipeline.py
pytest -q
streamlit run app/dashboard.py
```

Open `notebooks/collections_investigation.ipynb` in Jupyter/Colab for the analysis walkthrough. The original archive is preserved at `data/raw/credresolve_collections_dataset.zip`; the pipeline extracts it to `data/source/` and writes outputs to `outputs/`.

## Generated outputs

- `data_quality_report.csv`: per-table row counts, exact duplicates and missingness.
- `golden_payments.csv`: canonicalized payment events joined to available account attributes.
- `monthly_recovery_metrics.csv`: gross successful collections and paid-account counts by UTC month.
- `payment_status_audit.csv`, `source_inventory.csv`: audit support.

## Key finding

The supplied extract shows July gross successful payments 6.48% above June; January to July is essentially flat (+0.01%). August is partial. This does **not** validate an 11% recovery-rate improvement: the extract lacks an approved eligible-balance denominator and reliable intervention-cost/counterfactual data. See `docs/executive_memo.md`.

## Method and limitations

Exact-row deduplication is reported for every table. Payment events are deduplicated using account + payment reference (fallback payment ID), latest event timestamp retained. Statuses are normalized; only successful statuses with positive amount and valid UTC event timestamp enter the monthly total. This is a transparent working definition, not a substitute for finance-approved settlement reconciliation. Do not infer channel causality.
