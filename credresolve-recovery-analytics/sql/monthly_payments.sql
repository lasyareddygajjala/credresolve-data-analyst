-- Run after importing outputs/golden_payments.csv into SQLite as golden_payments.
SELECT
  substr(event_at, 1, 7) AS month_utc,
  SUM(CASE WHEN upper(status_norm) IN ('SUCCESS','SUCCESSFUL','SETTLED','COMPLETED','PAID')
            AND CAST(amount AS REAL) > 0 THEN CAST(amount AS REAL) ELSE 0 END) AS successful_payment_amount,
  COUNT(DISTINCT CASE WHEN upper(status_norm) IN ('SUCCESS','SUCCESSFUL','SETTLED','COMPLETED','PAID')
                       AND CAST(amount AS REAL) > 0 THEN payment_id END) AS payment_count,
  COUNT(DISTINCT CASE WHEN upper(status_norm) IN ('SUCCESS','SUCCESSFUL','SETTLED','COMPLETED','PAID')
                       AND CAST(amount AS REAL) > 0 THEN account_id END) AS accounts_paid
FROM golden_payments
GROUP BY substr(event_at, 1, 7)
ORDER BY month_utc;
