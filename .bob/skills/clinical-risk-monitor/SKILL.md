---
name: clinical-risk-monitor
description: Analyze synthetic clinical trial records against the TrialGuard protocol, prioritize site risk, explain evidence, and draft CAPA actions. Use when a user asks for trial risk monitoring, protocol deviation analysis, site prioritization, or CAPA drafting in this project.
---

# TrialGuard Clinical Risk Monitor

## Guardrails
- Use synthetic or de-identified records only.
- Never invent patient facts.
- Treat severity as configurable project logic, not a universal regulatory definition.
- Do not make medical decisions or claim regulatory compliance.
- Keep an evidence trail from every finding to the record and protocol rule.
- Require human Clinical Operations / Quality review before any action.

## Workflow
1. Read `src/protocol.json`.
2. Read the supplied patient-record CSV.
3. Run the TrialGuard MCP analysis tool when available.
4. Group findings by site and patient.
5. Highlight major findings first.
6. Explain the exact record evidence and protocol rule.
7. Prioritize sites using the computed risk score and leading indicators.
8. Draft CAPA actions with owner/due-date placeholders.
9. State limitations and unresolved questions.

## Preferred output
- Executive summary
- Top-risk sites
- Major deviations
- Evidence table
- Recommended mitigations
- CAPA draft
- Human-review checkpoints
