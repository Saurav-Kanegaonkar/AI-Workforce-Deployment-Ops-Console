import csv
import json
import random
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "analysis" / "outputs"
SRC = ROOT / "src"

random.seed(42)

WORKFLOWS = [
    "appointment scheduling",
    "delivery tracking",
    "exception management",
    "vendor coordination",
    "maintenance intake",
    "collections follow-up",
]

SEGMENTS = ["enterprise logistics", "industrial services", "field operations", "customer operations"]
REGIONS = ["North America", "EMEA", "LATAM", "APAC"]
SYSTEM_STACKS = ["TMS + voice", "WMS + email", "dispatch + SMS", "CRM + voice", "ERP + webhook"]
OWNERS = ["Product Ops", "Deployment", "Product Engineering", "GTM Enablement"]
CAPABILITIES = ["voice", "reasoning", "coding", "workflow tools"]
PRODUCT_AREAS = ["voice stack", "orchestration", "integrations", "evals", "operator console"]


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def pct(value):
    return round(value, 1)


def build_deployments():
    rows = []
    for i in range(1, 29):
        workflow = random.choice(WORKFLOWS)
        stage = random.choices(
            ["discovery", "staging", "pilot", "production", "expansion"],
            weights=[2, 4, 6, 10, 6],
        )[0]
        automation = random.uniform(48, 93)
        eval_pass = random.uniform(72, 97)
        integration = random.uniform(58, 96)
        escalation = random.uniform(4, 28)
        label_coverage = random.uniform(42, 95)
        arr_band = random.choice(["250k-500k", "500k-1m", "1m-3m", "3m+"])
        rows.append(
            {
                "deployment_id": f"DEP{i:03d}",
                "account_segment": random.choice(SEGMENTS),
                "workflow": workflow,
                "region": random.choice(REGIONS),
                "system_stack": random.choice(SYSTEM_STACKS),
                "stage": stage,
                "owner": random.choice(OWNERS),
                "launch_week": (date(2026, 2, 2) + timedelta(days=7 * random.randint(0, 11))).isoformat(),
                "arr_band": arr_band,
                "weekly_contact_volume": random.randint(2200, 28000),
                "automation_coverage_pct": pct(automation),
                "eval_pass_rate_pct": pct(eval_pass),
                "integration_readiness_pct": pct(integration),
                "label_coverage_pct": pct(label_coverage),
                "open_escalations": int(round(escalation / 4)),
                "manual_hours_remaining": random.randint(18, 240),
            }
        )
    return rows


def build_releases(deployments):
    feature_names = [
        "carrier check-call reason codes",
        "multi-lingual voice fallback",
        "staging eval regression suite",
        "dispatcher handoff summary",
        "webhook retry policy",
        "quote confidence packaging",
        "maintenance vendor routing",
        "agent memory conflict detector",
        "deployment release notes digest",
        "operator console escalation queue",
        "collections promise-to-pay verifier",
        "coding agent runbook validator",
    ]
    rows = []
    for i, name in enumerate(feature_names, start=1):
        phase = random.choice(["design review", "staging", "limited release", "general enablement"])
        docs_ready = random.uniform(45, 100)
        eval_pass = random.uniform(68, 98)
        field_training = random.uniform(38, 96)
        blocked = random.sample(deployments, random.randint(2, 6))
        packaging = random.choice(["clear", "needs value metric", "needs guardrails", "not priced"])
        rows.append(
            {
                "feature_id": f"FEAT{i:03d}",
                "feature_name": name,
                "capability": random.choice(CAPABILITIES),
                "release_phase": phase,
                "owner": random.choice(OWNERS),
                "docs_ready_pct": pct(docs_ready),
                "eval_pass_rate_pct": pct(eval_pass),
                "field_training_pct": pct(field_training),
                "deployments_blocked": len(blocked),
                "blocked_deployment_ids": ";".join(row["deployment_id"] for row in blocked),
                "gtm_motion": random.choice(["new workflow", "expansion", "renewal defense", "pilot conversion"]),
                "price_packaging_status": packaging,
            }
        )
    return rows


def build_feedback(deployments, releases):
    rows = []
    start = date(2026, 3, 2)
    for i in range(1, 241):
        dep = random.choice(deployments)
        feature = random.choice(releases)
        severity = random.choices(["low", "medium", "high", "critical"], weights=[8, 11, 6, 2])[0]
        signal = random.choice(
            ["eval failure", "customer escalation", "deployment blocker", "sales question", "label drift", "integration defect"]
        )
        impact = {
            "low": random.randint(500, 2500),
            "medium": random.randint(2500, 12000),
            "high": random.randint(12000, 42000),
            "critical": random.randint(42000, 95000),
        }[severity]
        rows.append(
            {
                "feedback_id": f"FDBK{i:04d}",
                "event_date": (start + timedelta(days=random.randint(0, 55))).isoformat(),
                "deployment_id": dep["deployment_id"],
                "channel": random.choice(["field call", "Slack escalation", "QA review", "sales enablement", "customer ops review"]),
                "signal_type": signal,
                "severity": severity,
                "product_area": random.choice(PRODUCT_AREAS),
                "customer_impact_usd": impact,
                "time_to_triage_hours": pct(random.uniform(1, 42)),
                "status": random.choice(["new", "triaged", "in progress", "waiting on data", "closed"]),
                "linked_feature_id": feature["feature_id"],
                "product_action": random.choice(
                    [
                        "write release note",
                        "update eval case",
                        "patch integration",
                        "train deployment team",
                        "clarify pricing guardrail",
                        "escalate to product review",
                    ]
                ),
            }
        )
    return rows


def build_labeling_batches():
    rows = []
    for week in range(1, 9):
        for capability in CAPABILITIES:
            target = random.randint(1100, 2600)
            actual = int(target * random.uniform(0.72, 1.18))
            qa = random.uniform(82, 98)
            consensus = random.uniform(76, 96)
            rework = max(2, 100 - qa + random.uniform(0, 6))
            backlog = random.randint(250, 2400)
            rows.append(
                {
                    "batch_id": f"LBL{week:02d}-{capability.replace(' ', '').upper()}",
                    "week_start": (date(2026, 3, 2) + timedelta(days=7 * (week - 1))).isoformat(),
                    "capability": capability,
                    "vendor_type": random.choice(["in-house", "specialist agency", "hybrid"]),
                    "active_labelers": random.randint(4, 22),
                    "items_labeled": actual,
                    "throughput_target": target,
                    "qa_accept_rate_pct": pct(qa),
                    "consensus_rate_pct": pct(consensus),
                    "rework_rate_pct": pct(rework),
                    "backlog_items": backlog,
                    "dominant_failure_mode": random.choice(
                        ["ambiguous policy", "audio quality", "tool call mismatch", "edge-case reasoning", "missing customer context"]
                    ),
                }
            )
    return rows


def build_gtm_enablement():
    rows = []
    for i, workflow in enumerate(WORKFLOWS, start=1):
        for segment in SEGMENTS:
            sales = random.uniform(42, 96)
            technical = random.uniform(48, 98)
            quote_blocked = sales < 68 or technical < 70 or random.random() < 0.18
            rows.append(
                {
                    "package_id": f"GTM{i:02d}-{segment.split()[0].upper()}",
                    "segment": segment,
                    "workflow": workflow,
                    "pricing_model": random.choice(["per resolved workflow", "per contact", "platform plus usage", "pilot fee plus expansion"]),
                    "value_metric": random.choice(["manual hours removed", "autonomous resolution", "late delivery reduction", "cost per completed workflow"]),
                    "sales_confidence_pct": pct(sales),
                    "technical_confidence_pct": pct(technical),
                    "missing_artifacts": random.choice(
                        ["ROI calculator", "security FAQ", "integration checklist", "pricing guardrail", "case study proof", "none"]
                    ),
                    "quote_blocked": "yes" if quote_blocked else "no",
                    "enabled_reps": random.randint(3, 28),
                }
            )
    return rows


def score_deployments(deployments, feedback):
    feedback_by_deployment = defaultdict(lambda: {"count": 0, "impact": 0, "critical": 0, "triage": 0.0})
    for row in feedback:
        bucket = feedback_by_deployment[row["deployment_id"]]
        bucket["count"] += 1
        bucket["impact"] += int(row["customer_impact_usd"])
        bucket["triage"] += float(row["time_to_triage_hours"])
        if row["severity"] in {"high", "critical"}:
            bucket["critical"] += 1

    rows = []
    for dep in deployments:
        signals = feedback_by_deployment[dep["deployment_id"]]
        readiness = (
            float(dep["automation_coverage_pct"]) * 0.28
            + float(dep["eval_pass_rate_pct"]) * 0.28
            + float(dep["integration_readiness_pct"]) * 0.24
            + float(dep["label_coverage_pct"]) * 0.20
        )
        escalation = (
            signals["critical"] * 9
            + signals["count"] * 1.6
            + signals["impact"] / 18000
            + int(dep["manual_hours_remaining"]) / 22
            + int(dep["open_escalations"]) * 3
        )
        risk = max(0, 100 - readiness) * 0.65 + escalation
        if readiness < 74:
            action = "run readiness review with deployment and product engineering"
        elif signals["critical"] >= 3:
            action = "escalate field feedback into release planning"
        elif float(dep["label_coverage_pct"]) < 68:
            action = "increase labeling coverage before expansion"
        else:
            action = "prepare expansion brief and GTM enablement"
        rows.append(
            {
                "deployment_id": dep["deployment_id"],
                "workflow": dep["workflow"],
                "stage": dep["stage"],
                "owner": dep["owner"],
                "readiness_score": pct(readiness),
                "escalation_score": pct(escalation),
                "priority_score": pct(risk),
                "high_severity_signals": signals["critical"],
                "customer_impact_usd": int(signals["impact"]),
                "recommended_action": action,
            }
        )
    return sorted(rows, key=lambda row: float(row["priority_score"]), reverse=True)


def score_releases(releases):
    rows = []
    for row in releases:
        risk = (
            (100 - float(row["docs_ready_pct"])) * 0.28
            + (100 - float(row["eval_pass_rate_pct"])) * 0.35
            + (100 - float(row["field_training_pct"])) * 0.26
            + int(row["deployments_blocked"]) * 3.2
        )
        if row["price_packaging_status"] != "clear":
            risk += 8
        rows.append({**row, "release_risk_score": pct(risk)})
    return sorted(rows, key=lambda row: float(row["release_risk_score"]), reverse=True)


def score_labeling(rows):
    grouped = defaultdict(lambda: {"items": 0, "target": 0, "qa": 0.0, "consensus": 0.0, "rework": 0.0, "backlog": 0, "rows": 0})
    for row in rows:
        bucket = grouped[row["capability"]]
        bucket["items"] += int(row["items_labeled"])
        bucket["target"] += int(row["throughput_target"])
        bucket["qa"] += float(row["qa_accept_rate_pct"])
        bucket["consensus"] += float(row["consensus_rate_pct"])
        bucket["rework"] += float(row["rework_rate_pct"])
        bucket["backlog"] += int(row["backlog_items"])
        bucket["rows"] += 1

    summary = []
    for capability, values in grouped.items():
        throughput = values["items"] / values["target"] * 100
        qa = values["qa"] / values["rows"]
        consensus = values["consensus"] / values["rows"]
        rework = values["rework"] / values["rows"]
        risk = max(0, 100 - throughput) * 0.35 + max(0, 92 - qa) * 1.3 + max(0, 88 - consensus) + rework * 0.7 + values["backlog"] / 1400
        summary.append(
            {
                "capability": capability,
                "items_labeled": values["items"],
                "throughput_attainment_pct": pct(throughput),
                "qa_accept_rate_pct": pct(qa),
                "consensus_rate_pct": pct(consensus),
                "rework_rate_pct": pct(rework),
                "backlog_items": values["backlog"],
                "labeling_risk_score": pct(risk),
            }
        )
    return sorted(summary, key=lambda row: float(row["labeling_risk_score"]), reverse=True)


def score_gtm(rows):
    scored = []
    for row in rows:
        risk = (100 - float(row["sales_confidence_pct"])) * 0.42 + (100 - float(row["technical_confidence_pct"])) * 0.46
        if row["quote_blocked"] == "yes":
            risk += 12
        if row["missing_artifacts"] != "none":
            risk += 7
        scored.append({**row, "gtm_readiness_risk": pct(risk)})
    return sorted(scored, key=lambda row: float(row["gtm_readiness_risk"]), reverse=True)


def write_data_js(deployment_queue, release_queue, labeling_summary, gtm_queue, feedback):
    high_feedback = sorted(
        feedback,
        key=lambda row: (row["severity"] == "critical", row["severity"] == "high", int(row["customer_impact_usd"])),
        reverse=True,
    )[:12]
    kpis = {
        "deploymentReadiness": pct(sum(float(row["readiness_score"]) for row in deployment_queue) / len(deployment_queue)),
        "releaseRisk": pct(sum(float(row["release_risk_score"]) for row in release_queue[:6]) / 6),
        "labelingThroughput": pct(sum(float(row["throughput_attainment_pct"]) for row in labeling_summary) / len(labeling_summary)),
        "blockedQuotes": sum(1 for row in gtm_queue if row["quote_blocked"] == "yes"),
        "highSeveritySignals": sum(int(row["high_severity_signals"]) for row in deployment_queue),
        "customerImpact": sum(int(row["customer_impact_usd"]) for row in deployment_queue),
    }
    payload = {
        "kpis": kpis,
        "deploymentQueue": deployment_queue[:10],
        "releaseQueue": release_queue[:8],
        "labelingSummary": labeling_summary,
        "gtmQueue": gtm_queue[:10],
        "feedbackLoop": high_feedback,
    }
    SRC.mkdir(exist_ok=True)
    (SRC / "data.js").write_text("export const opsData = " + json.dumps(payload, indent=2) + ";\n")


def write_analysis_docs(deployment_queue, release_queue, labeling_summary, gtm_queue):
    top_dep = deployment_queue[0]
    top_release = release_queue[0]
    top_label = labeling_summary[0]
    top_gtm = gtm_queue[0]
    (ROOT / "analysis").mkdir(exist_ok=True)
    (ROOT / "analysis" / "analysis_plan.md").write_text(
        """# Analysis Plan

1. Normalize deployment, release, field feedback, labeling, and GTM enablement data to shared operating grains.
2. Score deployment readiness from automation coverage, evaluation pass rate, integration readiness, and label coverage.
3. Score release risk from documentation, eval performance, deployment blockers, field training, and pricing readiness.
4. Score labeling operations from throughput attainment, QA acceptance, consensus, rework, and backlog.
5. Convert high-risk records into an operating queue with clear owners and next actions.
"""
    )
    (ROOT / "analysis" / "executive_findings.md").write_text(
        f"""# Executive Findings

## What I Analyzed

I modeled a product operations system for enterprise AI worker deployments across release readiness, deployment execution, field feedback, labeling throughput, and GTM enablement.

## Findings

- Highest deployment priority: {top_dep['deployment_id']} on {top_dep['workflow']} with a priority score of {top_dep['priority_score']}.
- Highest release risk: {top_release['feature_name']} with {top_release['deployments_blocked']} blocked deployments and a risk score of {top_release['release_risk_score']}.
- Highest labeling risk: {top_label['capability']} with {top_label['throughput_attainment_pct']}% throughput attainment and {top_label['backlog_items']} backlog items.
- Highest GTM readiness risk: {top_gtm['workflow']} for {top_gtm['segment']} because {top_gtm['missing_artifacts']} remains unresolved.

## Recommendation

Run a weekly deployment readiness review that starts with the priority queue, resolves release blockers, allocates labeling capacity, and updates GTM enablement artifacts before additional customer expansion.
"""
    )
    (ROOT / "analysis" / "methodology.md").write_text(
        """# Methodology

The scoring model is rules-based because the operating question is prioritization, not prediction. Each score is transparent enough for Product Engineering, Deployment, GTM, and Operations to challenge in a working session.

Deployment readiness combines automation coverage, evaluation pass rate, integration readiness, and label coverage. Escalation pressure adds high-severity field signals, estimated customer impact, open escalations, and manual hours remaining.

Release risk combines documentation readiness, eval pass rate, field training, blocked deployments, and pricing or packaging gaps.

Labeling risk combines throughput attainment, QA acceptance, consensus, rework, and backlog volume for voice, reasoning, coding, and workflow-tool labels.

GTM readiness risk combines sales confidence, technical confidence, quote blockers, and missing commercial artifacts.
"""
    )


def main():
    DATA.mkdir(exist_ok=True)
    OUTPUTS.mkdir(parents=True, exist_ok=True)

    deployments = build_deployments()
    releases = build_releases(deployments)
    feedback = build_feedback(deployments, releases)
    labeling = build_labeling_batches()
    gtm = build_gtm_enablement()

    deployment_queue = score_deployments(deployments, feedback)
    release_queue = score_releases(releases)
    labeling_summary = score_labeling(labeling)
    gtm_queue = score_gtm(gtm)

    write_csv(DATA / "deployments.csv", deployments, list(deployments[0].keys()))
    write_csv(DATA / "release_readiness.csv", releases, list(releases[0].keys()))
    write_csv(DATA / "field_feedback.csv", feedback, list(feedback[0].keys()))
    write_csv(DATA / "labeling_batches.csv", labeling, list(labeling[0].keys()))
    write_csv(DATA / "gtm_enablement.csv", gtm, list(gtm[0].keys()))

    write_csv(OUTPUTS / "deployment_priority_queue.csv", deployment_queue, list(deployment_queue[0].keys()))
    write_csv(OUTPUTS / "release_enablement_queue.csv", release_queue, list(release_queue[0].keys()))
    write_csv(OUTPUTS / "labeling_ops_summary.csv", labeling_summary, list(labeling_summary[0].keys()))
    write_csv(OUTPUTS / "gtm_readiness_queue.csv", gtm_queue, list(gtm_queue[0].keys()))

    write_data_js(deployment_queue, release_queue, labeling_summary, gtm_queue, feedback)
    write_analysis_docs(deployment_queue, release_queue, labeling_summary, gtm_queue)

    print("Generated synthetic operating data and analysis outputs.")
    print(f"Top deployment: {deployment_queue[0]['deployment_id']} with priority score {deployment_queue[0]['priority_score']}")
    print(f"Top release risk: {release_queue[0]['feature_name']} with risk score {release_queue[0]['release_risk_score']}")


if __name__ == "__main__":
    main()
