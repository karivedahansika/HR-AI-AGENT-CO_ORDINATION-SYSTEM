"""
REST API for HR AI Agents platform (Milestone 4).
Run: uvicorn api.main:app --reload --port 8000
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from orchestrator import process_message
from workflows.orchestrator_engine import get_metrics, get_run_history, COMPLEX_WORKFLOWS
from coordination.agent_roles import AGENT_ROLES
from foundation.langchain_setup import langchain_status

app = FastAPI(
    title="HR AI Agents API",
    description="Production API for multi-agent HR coordination platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple request log for monitoring
_API_LOG: List[Dict[str, Any]] = []


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    duration_ms: float
    session_id: Optional[str] = None


@app.get("/health")
def health():
    return {"status": "ok", "service": "hr-ai-agents", "version": "1.0.0"}


@app.get("/metrics")
def metrics():
    m = get_metrics()
    m["api_requests"] = len(_API_LOG)
    m["langchain"] = langchain_status()
    return m


@app.get("/runs")
def runs(limit: int = 20):
    return {"runs": get_run_history(limit)}


@app.get("/agents")
def list_agents():
    return {
        "agents": [
            {"key": k, "name": v["name"], "role": v["role"], "responsibilities": v["responsibilities"]}
            for k, v in AGENT_ROLES.items()
        ]
    }


@app.get("/workflows")
def list_workflows():
    return {
        "workflows": [
            {"key": k, "name": v["name"], "steps": len(v["steps"]), "keywords": v["keywords"]}
            for k, v in COMPLEX_WORKFLOWS.items()
        ]
    }


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    t0 = time.perf_counter()
    try:
        reply = process_message(req.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    duration = (time.perf_counter() - t0) * 1000
    _API_LOG.append({
        "message": req.message[:100],
        "duration_ms": duration,
        "session_id": req.session_id,
    })
    if len(_API_LOG) > 200:
        _API_LOG.pop(0)
    return ChatResponse(reply=reply, duration_ms=round(duration, 2), session_id=req.session_id)


@app.get("/")
def root():
    return {
        "message": "HR AI Agents API",
        "docs": "/docs",
        "health": "/health",
        "endpoints": ["/chat", "/metrics", "/runs", "/agents", "/workflows"],
    }
