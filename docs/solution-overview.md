# Solution Overview

TrialGuard AI has five layers:

1. **Protocol parser** — reads visit windows, dose requirements and prohibited medications.
2. **Deviation engine** — compares each record with the configured protocol.
3. **Severity layer** — maps finding types to configurable Major / Minor / Administrative labels.
4. **Risk engine** — aggregates leading indicators into a 0–100 site score and risk tier.
5. **CAPA layer** — turns evidence into recommended mitigation actions and a review-ready draft.

The key design principle is **traceability**. A risk score is not presented as a black box: users can drill down to the site, patient, visit, deviation type and evidence that produced the score.

IBM Bob is connected through a custom MCP server so Bob can invoke the same analysis and CAPA workflow from the project workspace. Bob's role is therefore useful for investigation and report drafting rather than being a decorative mention.
