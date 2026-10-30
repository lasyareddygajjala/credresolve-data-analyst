# Executive memo — recovery performance investigation

## Decision summary

**The supplied data does not substantiate a sustained 11% month-on-month improvement.** The reproducible payment view shows June 2026 gross successful payments of **₹17.59 Cr** and July of **₹18.72 Cr**, a **6.48%** increase. January to July is essentially flat (**+0.01%**). August contains only ₹4.71 Cr in the supplied extract and is treated as a partial month; it must not be compared with a full month. These are gross successful payment amounts, not a normalized recovery rate.

## What is directly observed (Fact)

- The source archive identifies itself as a **synthetic challenge dataset** (seed 42), with intentionally injected duplicates, missing values, mixed time zones, schema versions, legacy codes, late-arriving events and identifier inconsistencies.
- 17 CSV tables were loaded by the pipeline. The `payments` table has 25,500 raw rows and 486 exact duplicate rows; after exact-row deduplication it has 25,014 rows.
- Payment status counts in the raw file: SUCCESS 17,880; FAILED 3,744; PENDING 2,592; REVERSED 1,284.
- Monthly positive successful payment totals (UTC event month): Jan ₹18.72 Cr; Feb ₹17.03 Cr; Mar ₹18.92 Cr; Apr ₹17.52 Cr; May ₹18.43 Cr; Jun ₹17.59 Cr; Jul ₹18.72 Cr; Aug ₹4.71 Cr (partial/incomplete).
- July vs June gross successful payment amount is +6.48%, not +11%. Jan vs July is +0.01%.

## Interpretation (Strong evidence / limitations)

The reported 11% cannot be validated from this extract as a business recovery-rate claim. The extract spans January–August 2026, not a complete 12 months, and the August period is incomplete. The current pipeline uses UTC event time and a conservative status allow-list; this is a reproducible analytical definition, not proof that it matches the company's production ledger.

## Golden-layer policy

1. Preserve raw CSVs unchanged under `data/source/`; generated outputs are separate.
2. Remove exact duplicate rows at table level and report the row impact.
3. For payments, normalize status to uppercase/trimmed; count SUCCESS, SUCCESSFUL, SETTLED, COMPLETED and PAID as successful only where present. Require positive numeric amount and valid event timestamp for monthly gross collections.
4. Deduplicate payment events by `(account_id, payment_reference)` when a reference exists; otherwise retain `payment_id` as the event key. Keep the latest event timestamp. This is a pragmatic event de-duplication rule and should be reconciled against the payment processor's settlement ledger before financial reporting.
5. Parse event timestamps as UTC. Original timezone metadata is not consistently sufficient to reconstruct every local timestamp; UTC is used for consistent month bucketing and must be validated with source-system owners.
6. Join account attributes only for descriptive segmentation. Do not treat mutable current account attributes as historical truth.
7. Never infer missing contact/RPC/PTP/cost/agent-hour metrics. They require validated disposition mappings, PTP-to-payment matching, session overlap logic and cost data.

## ₹10 Cr recommendation

**Do not release the full ₹10 Cr on this evidence.** The data does not contain a validated incremental-cost model, controlled channel experiment, or reliable causal attribution. The defensible recommendation is a gated experiment rather than a single unconditional investment: run a randomized borrower-level test of improved targeting against business-as-usual, stratified by DPD, outstanding balance, geography and risk segment; measure incremental net settled collections, complaints/opt-outs, cost per incremental rupee and 30/60/90-day outcomes. Approve scale-up only after the lower confidence bound of incremental ROI clears the company's hurdle rate.

This does not claim targeting is proven best; it is the lowest-regret way to resolve the decision with the current evidence. A precise incremental recovery, ROI or break-even estimate cannot be calculated from the supplied tables without intervention costs and a credible counterfactual.

## Next data required

- Finance-approved opening eligible balance by month and account; write-offs, reversals, settlements and restructures.
- Immutable payment processor settlement IDs and reversal/refund linkage.
- Historical account-state snapshots, not only latest state.
- Canonical agent identity and session-level paid productive hours.
- Disposition-code mapping and verified RPC/contact definitions.
- Campaign assignment/exposure logs with treatment/control flags and cost by channel.
- Complete September–December (or the actual missing period) and an agreed reporting cutoff.

## Classification of conclusions

| Conclusion | Classification |
|---|---|
| Exact duplicate payment rows exist | Fact |
| July gross successful amount is 6.48% above June in this extract | Fact |
| The 11% business recovery-rate claim is not proven by the supplied data | Strong evidence |
| Any channel caused the monthly movement | Hypothesis — not established |
| ₹10 Cr should be fully deployed to a named channel today | Not supportable |
