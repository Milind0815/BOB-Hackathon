import io
import pandas as pd
import streamlit as st
import plotly.express as px
from engine import detect_deviations, score_sites, capa_report

st.set_page_config(page_title="TrialGuard AI", page_icon="🧬", layout="wide")
st.title("🧬 TrialGuard AI")
st.caption("Clinical Trial Risk Monitor & Protocol Deviation Detector — synthetic hackathon prototype")

with st.sidebar:
    st.header("Study")
    st.write("TG-001 • Protocol v1.0")
    uploaded = st.file_uploader("Upload patient visit CSV", type=["csv"])
    st.info("Use synthetic/de-identified data only for this prototype.")

@st.cache_data
def load_demo():
    return pd.read_csv("src/data/patient_records.csv")

records = pd.read_csv(uploaded) if uploaded else load_demo()
required = {"patient_id","site_id","visit","scheduled_day","actual_day","dose_mg","co_medications","field_complete"}
missing = required - set(records.columns)
if missing:
    st.error(f"Missing columns: {sorted(missing)}")
    st.stop()

devs = detect_deviations(records)
sites = score_sites(records, devs)

c1,c2,c3,c4 = st.columns(4)
c1.metric("Patient visits", len(records))
c2.metric("Deviations", len(devs))
c3.metric("Major deviations", int((devs.severity=="major").sum()))
c4.metric("High/Critical sites", int(sites.risk_tier.isin(["High","Critical"]).sum()))

st.subheader("Site Risk Overview")
fig = px.bar(sites, x="site_id", y="risk_score", color="risk_tier", range_y=[0,100],
             labels={"risk_score":"Risk score","site_id":"Site"})
st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Risk-ranked sites")
    st.dataframe(sites, use_container_width=True, hide_index=True)
with right:
    st.subheader("Deviation mix")
    mix = devs["deviation_type"].value_counts().reset_index()
    mix.columns = ["type","count"]
    if len(mix):
        st.plotly_chart(px.pie(mix, names="type", values="count", hole=.45), use_container_width=True)
    else:
        st.success("No deviations detected.")

st.subheader("Deviation Evidence")
if devs.empty:
    st.success("No protocol deviations detected.")
else:
    st.dataframe(devs, use_container_width=True, hide_index=True)

st.subheader("CAPA-ready Report")
site_choice = st.selectbox("Select site", sites.site_id.tolist())
report = capa_report(site_choice, sites, devs)
st.markdown(report)
st.download_button("Download CAPA draft", report, file_name=f"{site_choice}_CAPA.md", mime="text/markdown")

st.divider()
st.caption("Prototype only. Severity and risk scoring must be reviewed against the sponsor's approved SOP and study-specific protocol before real-world use.")
