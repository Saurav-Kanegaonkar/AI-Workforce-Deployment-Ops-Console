# Data Dictionary

| Table | Grain | Purpose |
|---|---|---|
| `deployments.csv` | Deployment | Tracks workflow, stage, system stack, contact volume, readiness signals, open escalations, and remaining manual work. |
| `release_readiness.csv` | Product feature | Tracks feature readiness across documentation, evals, deployment blockers, field training, GTM motion, and pricing status. |
| `field_feedback.csv` | Feedback event | Captures production signals from the field with severity, product area, estimated customer impact, triage time, and linked feature. |
| `labeling_batches.csv` | Capability week | Captures labeling capacity, throughput, QA acceptance, consensus, rework, backlog, and dominant failure mode. |
| `gtm_enablement.csv` | Workflow package by segment | Tracks pricing model, value metric, sales confidence, technical confidence, missing artifacts, and quote blockers. |
| `deployment_priority_queue.csv` | Deployment | Derived queue that combines readiness and escalation pressure into a weekly operating priority. |
| `release_enablement_queue.csv` | Product feature | Derived queue that ranks release risk from docs, evals, field training, blockers, and pricing status. |
| `labeling_ops_summary.csv` | Capability | Derived summary of labeling throughput, quality, backlog, and risk by capability. |
| `gtm_readiness_queue.csv` | Workflow package by segment | Derived queue that ranks commercial readiness risk. |
