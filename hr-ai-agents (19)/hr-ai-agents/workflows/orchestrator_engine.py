"""
Complex workflow orchestration engine (Milestone 4).
Supports multi-step pipelines with status tracking and metrics.
"""

from datetime import datetime
from typing import List, Dict, Any, Callable, Optional
import time
import uuid


class WorkflowStep:
    def __init__(self, name: str, agent_key: str, description: str = ""):
        self.name = name
        self.agent_key = agent_key
        self.description = description
        self.status = "pending"  # pending | running | completed | failed
        self.started_at: Optional[str] = None
        self.finished_at: Optional[str] = None
        self.duration_ms: float = 0
        self.output: str = ""
        self.error: str = ""


class WorkflowRun:
    def __init__(self, workflow_name: str, user_input: str):
        self.id = str(uuid.uuid4())[:8]
        self.workflow_name = workflow_name
        self.user_input = user_input
        self.status = "pending"
        self.steps: List[WorkflowStep] = []
        self.started_at = datetime.utcnow().isoformat() + "Z"
        self.finished_at: Optional[str] = None
        self.total_duration_ms: float = 0


# In-memory run history for monitoring dashboard
_RUN_HISTORY: List[WorkflowRun] = []
_METRICS = {
    "total_runs": 0,
    "successful_runs": 0,
    "failed_runs": 0,
    "avg_duration_ms": 0.0,
    "tool_calls": 0,
    "agent_calls": 0,
}


def get_metrics() -> Dict[str, Any]:
    return dict(_METRICS)


def get_run_history(limit: int = 20) -> List[Dict[str, Any]]:
    out = []
    for r in _RUN_HISTORY[-limit:]:
        out.append({
            "id": r.id,
            "workflow": r.workflow_name,
            "status": r.status,
            "input": r.user_input[:80],
            "duration_ms": round(r.total_duration_ms, 1),
            "steps": len(r.steps),
            "started_at": r.started_at,
        })
    return list(reversed(out))


# Complex enterprise workflows
COMPLEX_WORKFLOWS = {
    "new_hire_pipeline": {
        "name": "New Hire Pipeline",
        "keywords": ["hire and onboard", "new hire pipeline", "recruit and onboard", "full hiring process"],
        "steps": [
            ("JD & Screening", "talent_acquisition", "Create role profile and screening guidance"),
            ("Onboarding Plan", "employee_lifecycle", "Generate onboarding checklist"),
            ("Policy & Compliance", "hr_ops_compliance", "Confirm leave and policy setup"),
        ],
    },
    "employee_exit_pipeline": {
        "name": "Employee Exit Pipeline",
        "keywords": ["full exit", "resignation process", "offboard and settle", "exit pipeline"],
        "steps": [
            ("Offboarding", "employee_lifecycle", "Exit checklist and handover"),
            ("Leave & Settlement", "hr_ops_compliance", "Leave balance and policy checks"),
        ],
    },
    "promotion_pipeline": {
        "name": "Promotion Pipeline",
        "keywords": ["promotion pipeline", "promotion process", "promote employee full"],
        "steps": [
            ("Performance Review", "performance_growth", "Review readiness and feedback"),
            ("Role Change", "employee_lifecycle", "Transfer / role change steps"),
            ("Policy Check", "hr_ops_compliance", "Compensation/policy alignment"),
        ],
    },
    "interview_to_offer": {
        "name": "Interview to Offer Pipeline",
        "keywords": ["interview to offer", "close candidate", "from interview to hire"],
        "steps": [
            ("Interview Prep", "talent_acquisition", "Questions and evaluation"),
            ("Compliance", "hr_ops_compliance", "Offer-related policy checks"),
        ],
    },
}


class WorkflowEngine:
    """Executes complex multi-step workflows with monitoring hooks."""

    def __init__(self, agent_handlers: Dict[str, Callable]):
        self.handlers = agent_handlers

    def detect(self, user_message: str) -> Optional[dict]:
        msg = user_message.lower()
        for key, wf in COMPLEX_WORKFLOWS.items():
            if any(k in msg for k in wf["keywords"]):
                return {"key": key, **wf}
        return None

    def run(self, workflow: dict, user_message: str, memory_context: str = "") -> str:
        run = WorkflowRun(workflow["name"], user_message)
        run.status = "running"
        t0 = time.perf_counter()

        for name, agent_key, desc in workflow["steps"]:
            step = WorkflowStep(name, agent_key, desc)
            step.status = "running"
            step.started_at = datetime.utcnow().isoformat() + "Z"
            run.steps.append(step)
            _METRICS["agent_calls"] += 1

            st = time.perf_counter()
            try:
                handler = self.handlers.get(agent_key)
                if not handler:
                    raise ValueError(f"Agent not found: {agent_key}")
                payload = user_message
                if memory_context:
                    payload = f"[Memory]\n{memory_context}\n\n{user_message}"
                # Pass previous step output as context
                prior = [s.output for s in run.steps[:-1] if s.output]
                if prior:
                    payload += "\n\n[Previous step output]\n" + prior[-1][:400]
                step.output = handler(payload)
                step.status = "completed"
            except Exception as e:
                step.status = "failed"
                step.error = str(e)
                step.output = f"**Step failed:** {e}"
                run.status = "failed"
            finally:
                step.duration_ms = (time.perf_counter() - st) * 1000
                step.finished_at = datetime.utcnow().isoformat() + "Z"

            if run.status == "failed":
                break

        run.total_duration_ms = (time.perf_counter() - t0) * 1000
        run.finished_at = datetime.utcnow().isoformat() + "Z"
        if run.status != "failed":
            run.status = "completed"
            _METRICS["successful_runs"] += 1
        else:
            _METRICS["failed_runs"] += 1
        _METRICS["total_runs"] += 1
        # rolling average
        n = _METRICS["total_runs"]
        _METRICS["avg_duration_ms"] = (
            (_METRICS["avg_duration_ms"] * (n - 1) + run.total_duration_ms) / n
        )
        _RUN_HISTORY.append(run)
        if len(_RUN_HISTORY) > 100:
            _RUN_HISTORY.pop(0)

        return self._format_result(run)

    def _format_result(self, run: WorkflowRun) -> str:
        lines = [
            f"**Workflow Automation:** {run.workflow_name}",
            f"**Run ID:** `{run.id}` · **Status:** {run.status} · **Duration:** {run.total_duration_ms:.0f} ms",
            "",
        ]
        for i, step in enumerate(run.steps, 1):
            icon = "✓" if step.status == "completed" else "✗"
            lines.append(f"### Step {i}: {step.name} [{icon} {step.status}] ({step.duration_ms:.0f} ms)")
            lines.append(step.output if step.output else step.error)
            lines.append("")
        lines.append("---\n*Tracked in monitoring dashboard / API metrics.*")
        return "\n".join(lines)
