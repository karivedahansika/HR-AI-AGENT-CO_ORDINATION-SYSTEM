import sys, os
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflows.orchestrator_engine import get_metrics, get_run_history, COMPLEX_WORKFLOWS
from coordination.agent_roles import AGENT_ROLES
from foundation.langchain_setup import langchain_status

st.set_page_config(page_title="Monitoring Dashboard", page_icon="📊", layout="wide")

st.markdown("""
<style>
.stApp { background: radial-gradient(ellipse at 30% 0%, #1a0a2e 0%, #0d0221 45%, #05010d 100%); color: #e8e6f0; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebarNav"] { display: none !important; }
h1, h2, h3 { color: #00f5ff !important; }
</style>
""", unsafe_allow_html=True)

st.title("📊 Monitoring Dashboard")
st.caption("Workflow runs · Performance metrics · System status")

m = get_metrics()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Workflow Runs", m.get("total_runs", 0))
c2.metric("Successful", m.get("successful_runs", 0))
c3.metric("Failed", m.get("failed_runs", 0))
c4.metric("Avg Duration (ms)", f"{m.get('avg_duration_ms', 0):.0f}")

c5, c6 = st.columns(2)
c5.metric("Agent Calls", m.get("agent_calls", 0))
c6.metric("Tool Calls", m.get("tool_calls", 0))

st.divider()
st.subheader("System Status")
lc = langchain_status()
st.json({
    "langchain_installed": lc.get("langchain_installed"),
    "mode": lc.get("mode"),
    "agents_registered": len(AGENT_ROLES),
    "workflows_registered": len(COMPLEX_WORKFLOWS),
})

st.subheader("Registered Workflows")
for k, wf in COMPLEX_WORKFLOWS.items():
    st.markdown(f"**{wf['name']}** — {len(wf['steps'])} steps · triggers: `{', '.join(wf['keywords'][:2])}`")

st.subheader("Recent Workflow Runs")
runs = get_run_history(15)
if not runs:
    st.info("No workflow runs yet. Try: `hire and onboard a new software engineer` in the main chat.")
else:
    st.dataframe(runs, use_container_width=True)

st.divider()
if st.button("Refresh metrics"):
    st.rerun()
if st.button("← Back to Home"):
    st.switch_page("app.py")
