# Assumptions and data decisions
1. Preserve the original ZIP unchanged.
2. Exact duplicate rows are counted and removed from staging.
3. Timestamps are parsed as UTC for consistent event-month reporting. This does not recover unknown original timezone semantics.
4. Payment records are provisionally deduplicated by account_id + payment_reference when reference exists; otherwise payment_id. Conflicting duplicate records must be reviewed in the audit before acceptance.
5. Successful status mapping is initially SUCCESS, SUCCESSFUL, SETTLED, COMPLETED, PAID. Review observed values.
6. Campaign attribution is not assigned to the latest interaction by default.
7. Missing IDs are not invented.
8. Findings must be labelled Fact, Strong Evidence, Correlation or Hypothesis.
