# Deployment Guide (Milestone 4)

## Local
```bash
pip install -r requirements.txt
python -m streamlit run app.py          # UI :8501
uvicorn api.main:app --reload --port 8000   # API :8000
```

## Docker
```bash
docker build -t hr-ai-agents .
docker run -p 8501:8501 hr-ai-agents
# API:
docker run -p 8000:8000 hr-ai-agents uvicorn api.main:app --host 0.0.0.0 --port 8000
```

## Docker Compose
```bash
docker-compose up --build
```
- Web UI: http://localhost:8501  
- API docs: http://localhost:8000/docs  

## Cloud options
- **Streamlit Community Cloud** – deploy `app.py` from GitHub  
- **Render / Railway / Fly.io** – use Dockerfile  
- **AWS / GCP / Azure** – container service with the same image  

Set `OPENAI_API_KEY` in environment for LLM mode (optional).
