```mermaid
flowchart LR
Raw[Original ZIP] --> Stage[CSV staging and profiling]
Stage --> Clean[Exact dedupe and timestamp parsing]
Clean --> Golden[Golden payments and account join]
Golden --> Metrics[Monthly metrics]
Metrics --> Dash[Streamlit dashboard]
Stage --> DQ[Data quality report]
```
Batch pipeline is appropriate for the assignment. Production additions: source contracts, incremental watermarks, late-event backfills, lineage, orchestration, access controls and metric monitoring.
