# HR-AI-AGENT-CO_ORDINATION-SYSTEM
# HR AI Agents – Enterprise Prototype

A working multi-agent HR system with:
- **HR Assistant** (central chatbot)
- 4 specialized agents:
  1. Talent Acquisition Agent
  2. Employee Lifecycle Agent
  3. Performance & Growth Agent
  4. HR Ops & Compliance Agent

## How to Run
cd hr-ai-agents
pip install -r requirements.txt
streamlit run app.py
Open the local URL shown in the terminal (usually http://localhost:8501).
How it works

You chat with the HR Assistant.
The system automatically routes your request to the most relevant agent(s).
The agent responds with structured, actionable HR guidance.
You can continue the conversation — context is maintained in the session.

Example Queries

"Write a job description for a Senior Data Analyst"
"Create an onboarding checklist for a new software engineer"
"Summarize performance review points for a team lead"
"What is our leave policy for maternity leave?"
"Help me screen this resume..."
"Prepare offboarding steps for an employee leaving next week"

Project Structure
hr-ai-agents/
├── app.py                  # Main Streamlit chatbot
├── orchestrator.py         # Routes queries to agents
├── agents/
│   ├── talent_acquisition.py
│   ├── employee_lifecycle.py
│   ├── performance_growth.py
│   └── hr_ops_compliance.py
├── utils/
│   └── helpers.py
├── requirements.txt
└── README.md
