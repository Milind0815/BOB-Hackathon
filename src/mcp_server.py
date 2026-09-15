import json
from pathlib import Path
import pandas as pd
from fastmcp import FastMCP
from engine import detect_deviations, score_sites, capa_report

mcp = FastMCP("TrialGuard Clinical Risk Monitor")
BASE = Path(__file__).resolve().parent

@mcp.tool()
def analyze_trial(records_csv_path: str) -> dict:
    """Analyze a synthetic/de-identified clinical trial CSV against the TrialGuard protocol.
    Returns deviation findings and site-level risk scores. Do not use for real patient data.
    """
    df = pd.read_csv(records_csv_path)
    devs = detect_deviations(df)
    sites = score_sites(df, devs)
    return {
        "deviations": devs.to_dict(orient="records"),
        "site_risk": sites.to_dict(orient="records")
    }

@mcp.tool()
def get_site_capa(site_id: str, records_csv_path: str) -> str:
    """Generate a CAPA-ready draft for one site from synthetic/de-identified trial data."""
    df = pd.read_csv(records_csv_path)
    devs = detect_deviations(df)
    sites = score_sites(df, devs)
    return capa_report(site_id, sites, devs)

@mcp.tool()
def explain_deviation(deviation_type: str, severity: str) -> str:
    """Explain a TrialGuard finding using the project's configured severity policy.
    This is a decision-support explanation, not regulatory or medical advice."""
    mapping = {
        "prohibited_medication": "Potential major deviation: a protocol-prohibited co-medication was recorded.",
        "dose_mismatch": "Potential major deviation: the recorded dose does not match the configured protocol dose.",
        "missed_visit": "Potential minor deviation: the visit was missed beyond the configured tolerance.",
        "out_of_window_visit": "Potential minor deviation: the visit occurred outside the configured visit window.",
        "missing_noncritical_field": "Administrative issue: a non-critical record field is incomplete."
    }
    return f"{mapping.get(deviation_type, 'Finding requires review.')} Configured severity: {severity}. Sponsor SOP and clinical/quality review control the final classification."

if __name__ == "__main__":
    mcp.run()
