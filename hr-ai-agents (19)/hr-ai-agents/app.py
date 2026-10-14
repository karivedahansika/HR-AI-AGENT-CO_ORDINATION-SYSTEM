import sys, os
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from orchestrator import process_message

st.set_page_config(
    page_title="HR Assistant",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp {
    background: radial-gradient(ellipse at 30% 0%, #1a0a2e 0%, #0d0221 45%, #05010d 100%);
    color: #e8e6f0;
}
#MainMenu, footer { visibility: hidden; }
div[data-testid="stToolbar"] { display: none; }
.block-container { padding-top: 1.5rem !important; max-width: 900px; }

/* Keep sidebar visible; only hide default multipage file list */
[data-testid="stSidebarNav"] { display: none !important; }
section[data-testid="stSidebar"] {
    display: flex !important;
    visibility: visible !important;
    min-width: 16rem;
}

.hero {
    text-align: center; padding: 1.5rem 1rem 1rem;
    animation: fadeIn 0.6s ease-out;
}
.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.1rem; font-weight: 700; margin: 0;
    background: linear-gradient(90deg, #ffffff 40%, #00f5ff 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero p { color: #7a8ba8; font-size: 0.88rem; margin-top: 0.35rem; }
.hero-line {
    width: 50px; height: 3px; margin: 0.7rem auto 0;
    background: linear-gradient(90deg, #ff2d95, #00f5ff);
    border-radius: 2px; animation: grow 0.7s ease-out 0.3s both;
}

div[data-testid="stChatMessage"] { animation: msgIn 0.4s ease-out; background: transparent !important; }
div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) [data-testid="stMarkdownContainer"] {
    background: rgba(20,10,45,0.9);
    border: 1px solid rgba(255,45,149,0.3);
    border-left: 3px solid #ff2d95;
    border-radius: 4px 14px 14px 14px;
    padding: 0.9rem 1.1rem;
}
div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) [data-testid="stMarkdownContainer"] {
    background: rgba(10,30,50,0.9);
    border: 1px solid rgba(0,245,255,0.25);
    border-radius: 14px 4px 14px 14px;
    padding: 0.9rem 1.1rem;
}
div[data-testid="stChatMessageAvatarAssistant"] {
    background: linear-gradient(135deg, #ff2d95, #c400ff) !important;
}
div[data-testid="stChatMessageAvatarUser"] {
    background: linear-gradient(135deg, #00f5ff, #0088aa) !important;
}
div[data-testid="stChatInput"] {
    background: rgba(15,10,35,0.9) !important;
    border: 1px solid rgba(0,245,255,0.25) !important;
    border-radius: 14px !important;
}
div[data-testid="stChatInput"]:focus-within {
    border-color: #00f5ff !important;
    box-shadow: 0 0 0 2px rgba(0,245,255,0.12);
}
div[data-testid="stChatInput"] textarea { color: #e8e6f0 !important; }

/* All sidebar buttons look the same */
.stButton > button {
    background: rgba(0,245,255,0.07) !important;
    color: #00f5ff !important;
    border: 1px solid rgba(0,245,255,0.3) !important;
    border-radius: 12px !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    padding: 0.6rem 1rem !important;
    transition: all 0.2s ease !important;
    width: 100%;
}
.stButton > button:hover {
    background: rgba(0,245,255,0.18) !important;
    border-color: #00f5ff !important;
    box-shadow: 0 0 12px rgba(0,245,255,0.2);
    transform: translateY(-1px);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0221, #1a0a2e) !important;
    border-right: 1px solid rgba(0,245,255,0.12);
}
section[data-testid="stSidebar"] h3 {
    color: #00f5ff !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    margin-bottom: 0.6rem !important;
}
.stSpinner > div { border-top-color: #00f5ff !important; }

@keyframes fadeIn { from { opacity:0; transform:translateY(-12px); } to { opacity:1; transform:none; } }
@keyframes grow { from { width:0; opacity:0; } to { width:50px; opacity:1; } }
@keyframes msgIn { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:none; } }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>HR Assistant</h1>
    <p>Multi-Agent System · AI Tools</p>
    <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar: Agents + Tools as same-style buttons ────────────────
with st.sidebar:
    st.markdown("### Agents")
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
    if st.button("📊  Monitoring Dashboard", use_container_width=True, key="nav_mon"):
        st.switch_page("pages/6_Monitoring_Dashboard.py")

    st.markdown("---")
    st.markdown("### AI Tools")
    if st.button("📄  Resume Screener", use_container_width=True, key="tool_resume"):
        st.session_state.pending_prompt = "Screen resume for Data Analyst"
    if st.button("❓  Interview Questions", use_container_width=True, key="tool_interview"):
        st.session_state.pending_prompt = "Generate interview questions for Software Engineer"
    if st.button("📅  Leave Balance", use_container_width=True, key="tool_leave"):
        st.session_state.pending_prompt = "Leave balance for Priya Sharma"
    if st.button("📜  Policy Checker", use_container_width=True, key="tool_policy"):
        st.session_state.pending_prompt = "Check maternity policy"
    if st.button("📋  Onboarding Plan", use_container_width=True, key="tool_onboard"):
        st.session_state.pending_prompt = "Generate onboarding plan for Software Engineer"

    st.markdown("---")
    st.markdown("### 📎 Upload file")
    st.caption("PDF · Image · Text · CSV")
    uploaded = st.file_uploader(
        "Upload resume or document",
        type=["pdf", "txt", "png", "jpg", "jpeg", "webp", "csv"],
        key="chat_file_upload",
        help="Upload a resume PDF/photo or HR document",
    )
    st.text_input(
        "What should I do with the file?",
        key="file_prompt",
        placeholder="Screen this resume for Data Analyst",
    )
    if uploaded is not None:
        st.success(f"Selected: {uploaded.name}")
        if st.button("Send file to chat", use_container_width=True, key="btn_use_file"):
            note = (st.session_state.get("file_prompt") or "").strip()
            st.session_state.pending_file = {
                "name": uploaded.name,
                "bytes": uploaded.getvalue(),
                "type": uploaded.type or "",
            }
            st.session_state.pending_prompt = note or f"Screen resume using uploaded file {uploaded.name}"
            st.rerun()

    st.markdown("---")
    if st.button("Clear Chat", use_container_width=True, key="btn_clear"):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.session_state.pending_file = None
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": (
            "Hello! I'm your **HR Assistant**.\n\n"
            "**Agents** coordinate on complex requests (e.g. hire and onboard).\n"
            "**Memory:** `remember policy X is Y` · `recall policy X` · `memory log`\n\n"
            "You can **upload a PDF or image** from the sidebar (resumes, documents).\n"
            "Ask about recruitment, onboarding, performance, or policies."
        )
    }]
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None
if "pending_file" not in st.session_state:
    st.session_state.pending_file = None

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("file_name"):
            st.caption(f"📎 Attached: {m['file_name']}")

prompt = None
file_meta = None
if st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None
    file_meta = st.session_state.pending_file
    st.session_state.pending_file = None
elif user_input := st.chat_input("Ask me anything... (or upload a file in the sidebar)"):
    prompt = user_input

if prompt:
    display_user = prompt
    process_prompt = prompt

    # If a file was attached, extract content and merge into prompt
    if file_meta:
        from utils.file_upload import extract_text_from_upload, build_prompt_with_file

        class _F:
            def __init__(self, name, data):
                self.name = name
                self._data = data
            def read(self):
                return self._data
            def seek(self, *_):
                pass

        fake = _F(file_meta["name"], file_meta["bytes"])
        file_text, status = extract_text_from_upload(fake)
        process_prompt = build_prompt_with_file(prompt, file_text, file_meta["name"])
        display_user = f"{prompt}\n\n📎 **{file_meta['name']}**\n_{status}_"

    st.session_state.messages.append({
        "role": "user",
        "content": display_user,
        "file_name": file_meta["name"] if file_meta else None,
    })
    with st.chat_message("user"):
        st.markdown(display_user)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = process_message(
                    process_prompt,
                    conversation_history=st.session_state.messages,
                )
            except Exception as e:
                response = f"Error: `{str(e)}`"
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
