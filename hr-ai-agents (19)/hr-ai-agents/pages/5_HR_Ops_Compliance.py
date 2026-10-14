import sys, os
import streamlit as st
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.hr_ops_compliance import handle

st.set_page_config(page_title="HR Ops & Compliance", page_icon="📋", layout="centered")
st.markdown("""<style>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@600;700&display=swap");
html, body, [class*="css"] { font-family: Inter, sans-serif; }
.stApp { background: radial-gradient(ellipse at 30% 0%, #1a0a2e 0%, #0d0221 45%, #05010d 100%); color: #e8e6f0; }
#MainMenu, footer, header { visibility: hidden; }
.agent-hero { text-align: center; padding: 1.8rem 1rem 1rem; animation: fadeIn 0.6s ease-out; }
.agent-hero .icon {
    font-size: 2.8rem; display: inline-block;
    animation: bounceIn 0.8s ease-out both, idle 3s ease-in-out 1s infinite;
    filter: drop-shadow(0 0 12px rgba(0,245,255,0.3));
}
.agent-hero h1 {
    font-family: Space Grotesk, sans-serif; font-size: 1.7rem; font-weight: 700; margin: 0.4rem 0 0.25rem;
    background: linear-gradient(90deg, #fff 40%, #00f5ff 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.agent-hero p { color: #7a8ba8; font-size: 0.85rem; margin: 0; }
.agent-line {
    width: 45px; height: 3px; margin: 0.7rem auto 0;
    background: linear-gradient(90deg, #ff2d95, #00f5ff);
    border-radius: 2px; animation: grow 0.6s ease-out 0.3s both;
}
div[data-testid="stChatMessage"] { animation: msgIn 0.4s ease-out; background: transparent !important; }
div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) [data-testid="stMarkdownContainer"] {
    background: rgba(20,10,45,0.9); border: 1px solid rgba(255,45,149,0.3);
    border-left: 3px solid #ff2d95; border-radius: 4px 14px 14px 14px; padding: 0.9rem 1.1rem;
}
div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) [data-testid="stMarkdownContainer"] {
    background: rgba(10,30,50,0.9); border: 1px solid rgba(0,245,255,0.25);
    border-radius: 14px 4px 14px 14px; padding: 0.9rem 1.1rem;
}
div[data-testid="stChatMessageAvatarAssistant"] { background: linear-gradient(135deg, #ff2d95, #c400ff) !important; }
div[data-testid="stChatMessageAvatarUser"] { background: linear-gradient(135deg, #00f5ff, #0088aa) !important; }
div[data-testid="stChatInput"] {
    background: rgba(15,10,35,0.9) !important; border: 1px solid rgba(0,245,255,0.25) !important; border-radius: 14px !important;
}
div[data-testid="stChatInput"]:focus-within { border-color: #00f5ff !important; box-shadow: 0 0 0 2px rgba(0,245,255,0.12); }
div[data-testid="stChatInput"] textarea { color: #e8e6f0 !important; }
.stSpinner > div { border-top-color: #00f5ff !important; }
@keyframes fadeIn { from { opacity:0; transform:translateY(-12px); } to { opacity:1; transform:none; } }
@keyframes bounceIn { 0% { opacity:0; transform:scale(0.3); } 60% { transform:scale(1.15); } 100% { opacity:1; transform:scale(1); } }
@keyframes idle { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-6px); } }
@keyframes grow { from { width:0; opacity:0; } to { width:45px; opacity:1; } }
@keyframes msgIn { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:none; } }

[data-testid="stSidebarNav"] { display: none !important; }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0221, #1a0a2e) !important;
    border-right: 1px solid rgba(0,245,255,0.12);
}
.stButton > button {
    background: rgba(0,245,255,0.07) !important;
    color: #00f5ff !important;
    border: 1px solid rgba(0,245,255,0.3) !important;
    border-radius: 12px !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    padding: 0.6rem 1rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: rgba(0,245,255,0.18) !important;
    border-color: #00f5ff !important;
    box-shadow: 0 0 12px rgba(0,245,255,0.2);
    transform: translateY(-1px);
}
section[data-testid="stSidebar"] h3 {
    color: #00f5ff !important;
    font-size: 0.75rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

</style>""", unsafe_allow_html=True)
st.markdown("""
<div class="agent-hero">
    <div class="icon">📋</div>
    <h1>HR Ops & Compliance</h1>
    <p>Leave · Policies · Benefits · Compliance</p>
    <div class="agent-line"></div>
</div>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("### Agents")
    if st.button("🏠  Home", use_container_width=True, key="nav_home"):
        st.switch_page("app.py")
    if st.button("💬  General Chatbot", use_container_width=True, key="nav_general"):
        st.switch_page("pages/1_General_Chatbot.py")
    if st.button("🎯  Talent Acquisition", use_container_width=True, key="nav_ta"):
        st.switch_page("pages/2_Talent_Acquisition.py")
    if st.button("🔄  Employee Lifecycle", use_container_width=True, key="nav_life"):
        st.switch_page("pages/3_Employee_Lifecycle.py")
    if st.button("📈  Performance & Growth", use_container_width=True, key="nav_perf"):
        st.switch_page("pages/4_Performance_Growth.py")
    if st.button("📋  HR Ops & Compliance", use_container_width=True, key="nav_ops"):
        st.switch_page("pages/5_HR_Ops_Compliance.py")


if "ops_messages" not in st.session_state:
    st.session_state["ops_messages"] = [{"role": "assistant", "content": """Hello! I handle leave, policies, benefits, and compliance. How can I help?"""}]

for m in st.session_state["ops_messages"]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Ask about leave, policy or benefits..."):
    st.session_state["ops_messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Working..."):
            response = handle(prompt)
        st.markdown(response)
    st.session_state["ops_messages"].append({"role": "assistant", "content": response})
