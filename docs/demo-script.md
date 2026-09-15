# 3–5 Minute Demo Script

## 0:00–0:30 — Problem
“Imagine a clinical trial with thousands of visits across hundreds of sites. The risk team cannot manually inspect every record fast enough. TrialGuard turns the protocol into executable checks.”

## 0:30–1:20 — Protocol
Show `src/protocol.json`.
Explain:
- Visit windows
- Required dose
- Prohibited co-medications
- Configurable severity mapping

## 1:20–2:15 — Detection
Open the dashboard.
Show:
- Total visits
- Total deviations
- Major deviations
- High/Critical sites

Open a major finding and point to the evidence.

## 2:15–3:00 — Site risk
Show the risk-ranked site table.
Explain that the score combines deviation burden and leading indicators rather than waiting for an audit finding.

## 3:00–3:45 — Bob
Open IBM Bob.
Ask it:
“Using the TrialGuard MCP server, analyze the synthetic records, explain why the highest-risk site is high risk, and draft CAPA actions.”

Approve the MCP tool call and show the evidence-backed response.

## 3:45–4:30 — CAPA
Return to the dashboard.
Select the highest-risk site.
Download/show the CAPA draft.

## Closing
“TrialGuard closes the loop from protocol to evidence to risk to action, while keeping the final clinical and quality decision with humans.”
