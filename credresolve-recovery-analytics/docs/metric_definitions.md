# Metric contract

| Metric | Definition for this prototype | Important caveat |
|---|---|---|
| Gross successful collections | Sum of positive amounts for allow-listed successful payment statuses, by UTC event month | Not net of refunds unless linked; not a recovery rate |
| Successful payment events | Distinct canonical payment event keys after de-duplication | Payment reference may be reused incorrectly; reconcile to processor ledger |
| Accounts paid | Distinct account IDs with at least one qualifying payment in month | Monthly counts are not additive across months |
| Recovery rate | Settled collections / opening eligible outstanding balance | Not calculated: approved denominator unavailable |
| Contact rate | Unique valid contacts / eligible unique borrower attempts | Requires validated call outcome mapping |
| RPC | Unique right-party contacts / eligible attempts | Requires disposition dictionary and identity validation |
| PTP rate | Valid promises / RPC | PTP validity and duplicate promise policy required |
| PTP kept rate | PTPs with qualifying settled payment by promised date + grace / due PTPs | Must link PTP to payment and define grace period |
| Recovery per account | Net settled amount / eligible accounts | Requires eligibility snapshot |
| Recovery per agent-hour | Net settled amount / productive logged-in hours | Requires session overlap and cost/time policy |
| Cost per ₹ recovered | Channel cost / net settled collections | Costs are not supplied |
| Channel conversion | Accounts with attributable net payment / exposed accounts | Requires exposure windows and counterfactual |

Relative MoM change is `(current month / previous month - 1) × 100`. Compare complete months only. The pipeline uses UTC for consistent bucketing; business-local reporting needs an approved timezone policy.
