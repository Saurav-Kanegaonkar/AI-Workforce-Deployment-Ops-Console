import { opsData } from "./data.js";

const formatNumber = new Intl.NumberFormat("en-US");
const formatCurrency = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  notation: "compact",
  maximumFractionDigits: 1,
});

const surfaceCopy = {
  cockpit:
    "Operating pulse for the weekly product ops review. It shows whether deployments, releases, labeling capacity, and GTM enablement are moving together.",
  releases:
    "Release enablement board for Product Engineering and Deployment. Each row turns a feature into the field work needed before broad rollout.",
  feedback:
    "Field feedback loop for production signals. It keeps customer impact, product area, severity, and the next action in one shared queue.",
  labeling:
    "Labeling operations workbench for voice, reasoning, coding, and workflow-tool labels. It exposes throughput, QA, consensus, rework, and backlog pressure.",
  gtm:
    "Commercial readiness board for pricing and sales enablement. It shows which workflow packages are blocked by missing artifacts or confidence gaps.",
};

const surfaceOrder = ["cockpit", "releases", "feedback", "labeling", "gtm"];
const surfaceLabels = {
  cockpit: "Cockpit",
  releases: "Releases",
  feedback: "Feedback",
  labeling: "Labeling",
  gtm: "GTM",
};

function byId(id) {
  return document.getElementById(id);
}

function riskClass(score) {
  if (Number(score) >= 60) return "risk-high";
  if (Number(score) >= 38) return "risk-watch";
  return "risk-good";
}

function pctBar(value) {
  const safe = Math.max(0, Math.min(100, Number(value)));
  return `
    <div class="bar" aria-label="${safe}%">
      <span style="width:${safe}%"></span>
    </div>
  `;
}

function renderKpis() {
  const k = opsData.kpis;
  byId("kpis").innerHTML = [
    ["Deployment readiness", `${k.deploymentReadiness}%`, "average readiness score"],
    ["Release risk", `${k.releaseRisk}`, "top six release blockers"],
    ["Labeling throughput", `${k.labelingThroughput}%`, "voice, reasoning, coding, tools"],
    ["Blocked quotes", k.blockedQuotes, "GTM packages needing action"],
    ["High severity signals", k.highSeveritySignals, "field feedback items"],
    ["Customer impact", formatCurrency.format(k.customerImpact), "modeled open signal value"],
  ]
    .map(
      ([label, value, note]) => `
        <article class="metric">
          <span>${label}</span>
          <strong>${value}</strong>
          <em>${note}</em>
        </article>
      `
    )
    .join("");
}

function renderCockpit() {
  const topDeployments = opsData.deploymentQueue.slice(0, 5);
  const topRelease = opsData.releaseQueue[0];
  const topLabel = opsData.labelingSummary[0];

  return `
    <section class="surface-grid surface-grid-main">
      <article class="panel panel-wide">
        <div class="panel-heading">
          <p class="eyebrow">Deployment priority queue</p>
          <h2>Where product ops should spend the next operating cycle</h2>
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Deployment</th>
                <th>Workflow</th>
                <th>Stage</th>
                <th>Readiness</th>
                <th>Priority</th>
                <th>Next action</th>
              </tr>
            </thead>
            <tbody>
              ${topDeployments
                .map(
                  (row) => `
                    <tr>
                      <td><strong>${row.deployment_id}</strong></td>
                      <td>${row.workflow}</td>
                      <td>${row.stage}</td>
                      <td>${pctBar(row.readiness_score)}<span class="mini">${row.readiness_score}%</span></td>
                      <td><span class="pill ${riskClass(row.priority_score)}">${row.priority_score}</span></td>
                      <td>${row.recommended_action}</td>
                    </tr>
                  `
                )
                .join("")}
            </tbody>
          </table>
        </div>
      </article>
      <article class="panel stack">
        <p class="eyebrow">Weekly review starter</p>
        <h2>Three decisions</h2>
        <div class="decision">
          <span>01</span>
          <p>Resolve ${topRelease.feature_name} before enabling ${topRelease.deployments_blocked} blocked deployments.</p>
        </div>
        <div class="decision">
          <span>02</span>
          <p>Move ${topLabel.capability} labeling capacity until backlog drops below the weekly risk threshold.</p>
        </div>
        <div class="decision">
          <span>03</span>
          <p>Convert high-severity field signals into eval cases, release notes, or integration patches within 24 hours.</p>
        </div>
      </article>
    </section>
  `;
}

function renderReleases() {
  return `
    <section class="surface-grid">
      ${opsData.releaseQueue
        .map(
          (row) => `
            <article class="panel release-card">
              <div class="panel-heading compact">
                <p class="eyebrow">${row.capability} / ${row.release_phase}</p>
                <h2>${row.feature_name}</h2>
              </div>
              <dl class="readiness-list">
                <div><dt>Docs</dt><dd>${pctBar(row.docs_ready_pct)}${row.docs_ready_pct}%</dd></div>
                <div><dt>Evals</dt><dd>${pctBar(row.eval_pass_rate_pct)}${row.eval_pass_rate_pct}%</dd></div>
                <div><dt>Field training</dt><dd>${pctBar(row.field_training_pct)}${row.field_training_pct}%</dd></div>
              </dl>
              <div class="card-footer">
                <span class="pill ${riskClass(row.release_risk_score)}">Risk ${row.release_risk_score}</span>
                <span>${row.deployments_blocked} deployments blocked</span>
                <span>${row.price_packaging_status}</span>
              </div>
            </article>
          `
        )
        .join("")}
    </section>
  `;
}

function renderFeedback() {
  return `
    <section class="surface-grid surface-grid-main">
      <article class="panel panel-wide">
        <div class="panel-heading">
          <p class="eyebrow">Production feedback loop</p>
          <h2>Signals that need product, deployment, or GTM action</h2>
        </div>
        <div class="timeline">
          ${opsData.feedbackLoop
            .map(
              (row) => `
                <article class="event-row">
                  <div>
                    <span class="date">${row.event_date}</span>
                    <strong>${row.signal_type}</strong>
                    <p>${row.product_area} on ${row.deployment_id}. Action: ${row.product_action}.</p>
                  </div>
                  <div class="event-meta">
                    <span class="pill ${row.severity === "critical" || row.severity === "high" ? "risk-high" : "risk-watch"}">${row.severity}</span>
                    <span>${formatCurrency.format(row.customer_impact_usd)}</span>
                    <span>${row.time_to_triage_hours}h triage</span>
                  </div>
                </article>
              `
            )
            .join("")}
        </div>
      </article>
      <article class="panel stack">
        <p class="eyebrow">Feedback discipline</p>
        <h2>Operating rule</h2>
        <p class="large-copy">Every high-severity field signal must leave behind one durable artifact: an eval case, a runbook update, a release note, a pricing guardrail, or an integration fix.</p>
        <div class="checklist">
          <span>Source linked</span>
          <span>Owner assigned</span>
          <span>Customer impact sized</span>
          <span>Next review dated</span>
        </div>
      </article>
    </section>
  `;
}

function renderLabeling() {
  return `
    <section class="surface-grid">
      ${opsData.labelingSummary
        .map(
          (row) => `
            <article class="panel label-card">
              <div class="panel-heading compact">
                <p class="eyebrow">Data labeling operations</p>
                <h2>${row.capability}</h2>
              </div>
              <div class="label-metrics">
                <div><span>Items labeled</span><strong>${formatNumber.format(row.items_labeled)}</strong></div>
                <div><span>Backlog</span><strong>${formatNumber.format(row.backlog_items)}</strong></div>
              </div>
              <dl class="readiness-list">
                <div><dt>Throughput</dt><dd>${pctBar(row.throughput_attainment_pct)}${row.throughput_attainment_pct}%</dd></div>
                <div><dt>QA accept</dt><dd>${pctBar(row.qa_accept_rate_pct)}${row.qa_accept_rate_pct}%</dd></div>
                <div><dt>Consensus</dt><dd>${pctBar(row.consensus_rate_pct)}${row.consensus_rate_pct}%</dd></div>
                <div><dt>Rework</dt><dd>${row.rework_rate_pct}%</dd></div>
              </dl>
              <span class="pill ${riskClass(row.labeling_risk_score)}">Risk ${row.labeling_risk_score}</span>
            </article>
          `
        )
        .join("")}
    </section>
  `;
}

function renderGtm() {
  return `
    <section class="surface-grid surface-grid-main">
      <article class="panel panel-wide">
        <div class="panel-heading">
          <p class="eyebrow">GTM and pricing enablement</p>
          <h2>Where commercial motion is blocked by technical reality</h2>
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Workflow</th>
                <th>Segment</th>
                <th>Pricing model</th>
                <th>Value metric</th>
                <th>Sales</th>
                <th>Technical</th>
                <th>Missing artifact</th>
              </tr>
            </thead>
            <tbody>
              ${opsData.gtmQueue
                .map(
                  (row) => `
                    <tr>
                      <td><strong>${row.workflow}</strong></td>
                      <td>${row.segment}</td>
                      <td>${row.pricing_model}</td>
                      <td>${row.value_metric}</td>
                      <td>${row.sales_confidence_pct}%</td>
                      <td>${row.technical_confidence_pct}%</td>
                      <td><span class="pill ${row.quote_blocked === "yes" ? "risk-high" : "risk-watch"}">${row.missing_artifacts}</span></td>
                    </tr>
                  `
                )
                .join("")}
            </tbody>
          </table>
        </div>
      </article>
      <article class="panel stack">
        <p class="eyebrow">Commercial translation</p>
        <h2>Enablement packet</h2>
        <div class="checklist">
          <span>Use case one-pager</span>
          <span>Integration checklist</span>
          <span>Eval proof points</span>
          <span>Pricing guardrails</span>
          <span>Deployment owner map</span>
        </div>
      </article>
    </section>
  `;
}

const renderers = {
  cockpit: renderCockpit,
  releases: renderReleases,
  feedback: renderFeedback,
  labeling: renderLabeling,
  gtm: renderGtm,
};

function setSurface(name, updateUrl = true) {
  byId("surface-copy").textContent = surfaceCopy[name];
  byId("surface-content").innerHTML = renderers[name]();
  document.querySelectorAll("[data-surface]").forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.surface === name));
  });
  if (updateUrl) {
    history.replaceState(null, "", `#${name}`);
  }
}

function setupTabs() {
  byId("surface-tabs").innerHTML = surfaceOrder
    .map((name) => `<button type="button" data-surface="${name}">${surfaceLabels[name]}</button>`)
    .join("");
  byId("surface-tabs").addEventListener("click", (event) => {
    const button = event.target.closest("[data-surface]");
    if (!button) return;
    setSurface(button.dataset.surface);
  });
  window.addEventListener("hashchange", () => {
    const nextSurface = location.hash.replace("#", "");
    if (surfaceOrder.includes(nextSurface)) {
      setSurface(nextSurface, false);
    }
  });
}

renderKpis();
setupTabs();
const initialSurface = surfaceOrder.includes(location.hash.replace("#", ""))
  ? location.hash.replace("#", "")
  : "cockpit";
setSurface(initialSurface, false);
