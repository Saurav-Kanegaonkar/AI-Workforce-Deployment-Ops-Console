-- Deployment readiness review
select
  deployment_id,
  workflow,
  stage,
  readiness_score,
  escalation_score,
  priority_score,
  recommended_action
from deployment_priority_queue
order by priority_score desc
limit 10;

-- Release blockers by owner
select
  owner,
  count(*) as feature_count,
  avg(release_risk_score) as avg_release_risk,
  sum(deployments_blocked) as blocked_deployments
from release_enablement_queue
group by 1
order by avg_release_risk desc;

-- Labeling throughput quality gate
select
  capability,
  throughput_attainment_pct,
  qa_accept_rate_pct,
  consensus_rate_pct,
  rework_rate_pct,
  labeling_risk_score
from labeling_ops_summary
where labeling_risk_score >= 20
order by labeling_risk_score desc;

-- GTM packages blocked by missing artifacts
select
  workflow,
  segment,
  pricing_model,
  value_metric,
  missing_artifacts,
  gtm_readiness_risk
from gtm_readiness_queue
where quote_blocked = 'yes'
order by gtm_readiness_risk desc;
