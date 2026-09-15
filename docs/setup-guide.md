# Setup Guide

## Prerequisites
- Python 3.11+
- Git
- IBM Bob for the Bob integration demo

## Install
```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
# .venv\Scripts\Activate.ps1
pip install -r src/requirements.txt
```

## Run the dashboard
```bash
streamlit run src/app.py
```

## Verify
1. Open the Streamlit URL.
2. Confirm the demo dashboard shows patient visits and deviations.
3. Confirm high-risk sites appear in the risk table.
4. Select a site and download its CAPA draft.

## Bob + MCP
Open the repository in IBM Bob and enable MCP servers. The project contains `.bob/mcp.json` pointing to `src/mcp_server.py`.

Ask Bob:
> Analyze the synthetic trial records using the TrialGuard MCP server. Show the highest-risk sites, the evidence behind each major deviation, and draft CAPA actions for the highest-risk site.

IBM Bob supports project-level MCP configuration and local stdio MCP servers. citeturn0search1turn0search6

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError` | Activate `.venv` and rerun `pip install -r src/requirements.txt` |
| Streamlit cannot find CSV | Run `streamlit run src/app.py` from the repository root |
| Bob cannot see MCP server | Enable MCP in Bob and verify `.bob/mcp.json` |
| MCP dependency error | Upgrade/install `fastmcp` and restart Bob |
| Blank risk table | Check that the CSV has all required columns |

## Fresh-machine test
Clone the repository into a new directory, create a fresh virtual environment, install requirements, run the app and follow the Bob MCP test above.
