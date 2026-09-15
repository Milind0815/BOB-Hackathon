import json
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
with open(BASE / "protocol.json", "r", encoding="utf-8") as f:
    PROTOCOL = json.load(f)

def _visit_rule(visit):
    return next(v for v in PROTOCOL["visits"] if v["visit"] == visit)

def detect_deviations(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, r in df.iterrows():
        rule = _visit_rule(r["visit"])
        actual = float(r["actual_day"])
        scheduled = float(r["scheduled_day"])
        delta = actual - scheduled

        if abs(delta) > rule["window_after"] if delta >= 0 else abs(delta) > rule["window_before"]:
            rows.append({
                "patient_id": r["patient_id"], "site_id": r["site_id"],
                "visit": r["visit"], "deviation_type": "missed_visit" if abs(delta) > 2 * max(rule["window_after"], rule["window_before"], 1) else "out_of_window_visit",
                "severity": "minor",
                "evidence": f"Scheduled day {scheduled}, actual day {actual}, allowed window -{rule['window_before']} / +{rule['window_after']} days.",
                "recommended_action": "Review reason, document deviation, assess impact and reinforce visit scheduling controls."
            })

        if float(r["dose_mg"]) not in PROTOCOL["dose"]["allowed_mg"]:
            rows.append({
                "patient_id": r["patient_id"], "site_id": r["site_id"],
                "visit": r["visit"], "deviation_type": "dose_mismatch",
                "severity": "major",
                "evidence": f"Recorded dose {r['dose_mg']} mg; protocol allows {PROTOCOL['dose']['allowed_mg']} mg.",
                "recommended_action": "Immediate clinical/quality review; verify patient safety, dosing records and site corrective action."
            })

        meds = str(r["co_medications"])
        if meds.lower() != "none":
            for banned in PROTOCOL["prohibited_medications"]:
                if banned.lower() in meds.lower():
                    rows.append({
                        "patient_id": r["patient_id"], "site_id": r["site_id"],
                        "visit": r["visit"], "deviation_type": "prohibited_medication",
                        "severity": "major",
                        "evidence": f"Prohibited co-medication '{banned}' recorded at {r['visit']}.",
                        "recommended_action": "Escalate for medical/quality review; confirm medication history and assess protocol impact."
                    })

        if int(r["field_complete"]) == 0:
            rows.append({
                "patient_id": r["patient_id"], "site_id": r["site_id"],
                "visit": r["visit"], "deviation_type": "missing_noncritical_field",
                "severity": "administrative",
                "evidence": "A non-critical record field is incomplete.",
                "recommended_action": "Complete the source/EDC field and verify the correction trail."
            })
    return pd.DataFrame(rows)

def score_sites(records: pd.DataFrame, deviations: pd.DataFrame) -> pd.DataFrame:
    sites = records["site_id"].unique()
    out = []
    for site in sites:
        r = records[records.site_id == site]
        d = deviations[deviations.site_id == site]
        total = len(r)
        dev_rate = len(d) / total if total else 0
        major = (d.severity == "major").sum()
        missed = d.deviation_type.isin(["missed_visit", "out_of_window_visit"]).sum()
        dose = (d.deviation_type == "dose_mismatch").sum()
        trend = 1 if len(d.tail(3)) >= 2 else 0

        score = min(100, round(
            35 * min(dev_rate / 0.25, 1) +
            30 * min(major / 3, 1) +
            15 * min(missed / 3, 1) +
            10 * min(dose / 2, 1) +
            10 * trend
        ))
        tier = "Critical" if score >= 75 else "High" if score >= 50 else "Moderate" if score >= 25 else "Low"
        out.append({
            "site_id": site, "risk_score": score, "risk_tier": tier,
            "records": total, "deviations": len(d), "major": major,
            "visit_issues": missed, "dose_issues": dose,
            "leading_indicator": "Rising recent deviation trend" if trend else "Stable / limited recent trend"
        })
    return pd.DataFrame(out).sort_values("risk_score", ascending=False)

def capa_report(site_id: str, sites: pd.DataFrame, deviations: pd.DataFrame) -> str:
    s = sites[sites.site_id == site_id].iloc[0]
    d = deviations[deviations.site_id == site_id]
    actions = []
    if (d.deviation_type == "prohibited_medication").any():
        actions.append("Review prohibited co-medication screening and retrain site staff.")
    if (d.deviation_type == "dose_mismatch").any():
        actions.append("Perform immediate dose reconciliation and targeted monitoring.")
    if d.deviation_type.isin(["missed_visit", "out_of_window_visit"]).any():
        actions.append("Review visit scheduling workflow, reminders and site workload.")
    if (d.severity == "administrative").any():
        actions.append("Close documentation gaps and verify data-entry controls.")
    if not actions:
        actions.append("Continue routine risk-based oversight and monitor trend.")
    lines = [
        f"# CAPA-ready draft — {site_id}",
        "",
        f"**Risk tier:** {s.risk_tier}  ",
        f"**Risk score:** {s.risk_score}/100  ",
        f"**Deviation count:** {s.deviations}  ",
        "",
        "## Evidence",
        d[["patient_id","visit","deviation_type","severity","evidence"]].to_markdown(index=False) if not d.empty else "No deviations.",
        "",
        "## Recommended Actions",
        *[f"- {a}" for a in actions],
        "",
        "## Verification",
        "- Assign an owner and due date in the sponsor QMS/CAPA workflow.",
        "- Confirm corrective action effectiveness using the next monitoring cycle.",
        "- Require human Clinical Operations / Quality review before execution."
    ]
    return "\n".join(lines)
