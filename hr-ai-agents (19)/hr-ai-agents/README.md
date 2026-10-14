# HR AI Agents – Full Platform (Milestones 1–4)

## Milestone 1 – Agent Foundation
- LangChain-ready foundation, prompt templates, 4 agents, Streamlit UI, tests

## Milestone 2 – Tool Integration
- 5 HR tools, tool router, API connectors (HRMS/Email), exception handling

## Milestone 3 – Coordination & Memory
- Agent roles, multi-agent coordination, short-term + long-term memory

## Milestone 4 – Workflow Automation & Deployment
- Complex workflow engine (`workflows/`)
- REST API (`api/main.py` – FastAPI)
- Monitoring dashboard (`pages/6_Monitoring_Dashboard.py`)
- Docker + docker-compose + `DEPLOY.md`
- Performance tests (`performance_test.py`)

## Run UI
```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

## Run API
```bash
uvicorn api.main:app --reload --port 8000
# Docs: http://localhost:8000/docs
```

## Docker
```bash
docker-compose up --build
```

## Tests
```bash
python tests_tools.py
python validate_coordination.py
python performance_test.py
```
