# Data Sources

This project uses deterministic synthetic data for an enterprise AI workforce deployment operating system. The data is fictional and does not represent any real company, customer, or deployment.

## Source Tables

- `deployments.csv`: 28 AI worker deployments with workflow, region, system stack, stage, contact volume, readiness signals, open escalations, and manual hours remaining.
- `release_readiness.csv`: 12 product features with capability, release phase, documentation readiness, eval pass rate, field training progress, blocked deployments, GTM motion, and pricing status.
- `field_feedback.csv`: 240 production-style feedback records from field calls, QA review, sales enablement, customer ops review, and escalation channels.
- `labeling_batches.csv`: 32 weekly labeling batches across voice, reasoning, coding, and workflow-tool capabilities.
- `gtm_enablement.csv`: 24 commercial enablement records covering workflow packages, pricing model, value metric, sales confidence, technical confidence, missing artifacts, and quote blockers.

## Derived Outputs

- `analysis/outputs/deployment_priority_queue.csv`: deployment readiness and escalation scoring.
- `analysis/outputs/release_enablement_queue.csv`: release risk scoring.
- `analysis/outputs/labeling_ops_summary.csv`: labeling throughput and quality scoring.
- `analysis/outputs/gtm_readiness_queue.csv`: GTM and pricing readiness scoring.

## Generation Method

Run `python3 scripts/score_operating_data.py` to regenerate the data. The generator uses a fixed random seed so the artifact is reproducible. It models common enterprise AI worker operating patterns: high-volume coordination workflows, staged release rollout, field escalation signals, human labeling capacity, eval quality, and commercial enablement gaps.
