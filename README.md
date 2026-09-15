# TrialGuard AI — Clinical Trial Risk Monitor & Protocol Deviation Detector

## Team
- **Team:** YOUR TEAM NAME
- **Track:** Pharma & Biotech
- **Lead:** Milind Soni
- **Members:** Meera Patel, Tirth Patel, Sahejad Pathan

## Problem Statement
Large clinical trials can generate thousands of patient visits across hundreds of sites. Risk teams need to identify emerging protocol problems before they become audit findings. Manual review of visit records can hide missed visits, incorrect dosing and prohibited co-medications until late in the study.

## Solution
**TrialGuard AI** converts the study protocol into machine-readable rules and compares patient visit records against those rules. It detects deviations, assigns a configurable severity, calculates a site risk score from leading indicators, and generates a CAPA-ready report.

The project is designed around **synthetic data only**. It is a decision-support prototype, not a replacement for clinical, medical, quality or regulatory review.

## Key Features
1. Protocol-aware deviation detection.
2. Major / Minor / Administrative severity classification.
3. Site-level risk scoring using deviation rate, major deviation burden, missed visits, dosing errors and recent trend.
4. CAPA-ready mitigation recommendations.
5. IBM Bob integration through MCP for protocol/risk analysis and report drafting.

## Tech Stack
- Python 3.11+
- Streamlit
- Pandas
- Plotly
- ReportLab
- FastMCP-compatible MCP server
- IBM Bob

## Quick Start

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r src/requirements.txt
streamlit run src/app.py
```

Open the local URL shown by Streamlit.

## Demo Data
The app starts with synthetic records in `src/data/`. No real patient information is included.

## Bob Integration
The project includes:
- `.bob/mcp.json` — project MCP configuration.
- `src/mcp_server.py` — tools for protocol comparison, site risk scoring and CAPA drafting.
- `.bob/skills/clinical-risk-monitor/SKILL.md` — reusable Bob workflow.

IBM Bob supports project-level MCP configuration and can connect to local MCP servers. See the official Bob documentation linked in the project architecture document.

## Safety / Regulatory Position
This prototype is for hackathon demonstration only. It does not make medical decisions, determine patient eligibility, or provide regulatory/legal advice. Severity labels are configurable and should be mapped to the sponsor's approved deviation management SOP and study-specific definitions before real-world use.

## Known Limitations
- Synthetic data only.
- Rule-based detection is intentionally transparent and deterministic.
- The prototype does not connect to a real EDC, CTMS or safety database.
- CAPA drafts require human Quality/Clinical Operations review.
- Severity mapping is configurable rather than a universal regulatory definition.

## What We're Most Proud Of
The strongest part of TrialGuard AI is the chain from **protocol -> evidence -> deviation -> site risk -> CAPA**. Each result is traceable to a rule and a record, making the dashboard useful for risk-based oversight rather than being a black-box score.
