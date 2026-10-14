import streamlit as st
from orchestrator import process_message

# Page config
st.set_page_config(
    page_title="HR Assistant | Enterprise AI Agents",
    page_icon="👔",
    layout="centered"
)

# Custom CSS for cleaner look
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
    }
    .main-header {
        text-align: center;
        padding: 1rem 0 0.5rem 0;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header"><h1>👔 HR Assistant</h1></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Enterprise AI Agents for HR • Talent • Lifecycle • Performance • Ops & Compliance</div>',
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.header("Agents Available")
    st.markdown("""
    **1. Talent Acquisition Agent**  
    Job descriptions, screening, interviews, offers

    **2. Employee Lifecycle Agent**  
    Onboarding, offboarding, transfers

    **3. Performance & Growth Agent**  
    Reviews, goals, feedback, development

    **4. HR Ops & Compliance Agent**  
    Leave, policies, benefits, employee relations
    """)
    st.divider()
    st.markdown("**How to use**")
    st.markdown("Just type naturally. The system routes your request to the right agent automatically.")
    st.divider()
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I'm your **HR Assistant**.\n\nI work with 4 specialized agents to help you with recruitment, onboarding, performance, policies, and more.\n\nHow can I help you today?"
        }
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about HR..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from orchestrator
    with st.chat_message("assistant"):
        with st.spinner("Routing to the right agent..."):
            response = process_message(prompt)
        st.markdown(response)

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
