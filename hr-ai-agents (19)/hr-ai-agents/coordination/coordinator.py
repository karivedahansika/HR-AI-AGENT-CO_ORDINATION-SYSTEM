"""
Agent communication and coordination.

Supports:
- Single-agent routing
- Multi-agent collaboration (when a query spans multiple domains)
- Shared memory context injection
"""

from typing import List, Dict, Callable, Optional
from coordination.agent_roles import AGENT_ROLES, get_role_card


# Collaboration patterns: query signals -> ordered list of agents to run
COLLAB_PATTERNS = [
    {
        "name": "new_hire_full",
        "keywords": ["new hire", "new joiner joining", "hire and onboard", "recruit and onboard"],
        "agents": ["talent_acquisition", "employee_lifecycle", "hr_ops_compliance"],
        "description": "Recruitment + onboarding + policy for a new hire",
    },
    {
        "name": "exit_full",
        "keywords": ["resign and settle", "full exit", "offboard and leave", "resignation process full"],
        "agents": ["employee_lifecycle", "hr_ops_compliance"],
        "description": "Offboarding + leave/policy for exit",
    },
    {
        "name": "promotion_path",
        "keywords": ["promotion", "promote employee", "role change and review"],
        "agents": ["performance_growth", "employee_lifecycle", "hr_ops_compliance"],
        "description": "Performance + role change + policy",
    },
    {
        "name": "interview_to_offer",
        "keywords": ["interview and offer", "from interview to hire", "close candidate"],
        "agents": ["talent_acquisition", "hr_ops_compliance"],
        "description": "Interview support + policy/offer compliance",
    },
]


class AgentMessage:
    """Message passed between agents during collaboration."""

    def __init__(self, from_agent: str, to_agent: str, content: str, msg_type: str = "context"):
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.content = content
        self.msg_type = msg_type  # context | request | result

    def format(self) -> str:
        return f"[{self.from_agent} → {self.to_agent}] {self.content[:150]}"


class Coordinator:
    """
    Coordinates specialized agents and optional multi-agent workflows.
    """

    def __init__(self, agent_handlers: Dict[str, Callable]):
        self.handlers = agent_handlers
        self.message_log: List[AgentMessage] = []

    def detect_collaboration(self, user_message: str) -> Optional[dict]:
        msg = user_message.lower()
        for pattern in COLLAB_PATTERNS:
            if any(k in msg for k in pattern["keywords"]):
                return pattern
        return None

    def send(self, from_agent: str, to_agent: str, content: str, msg_type: str = "context") -> None:
        self.message_log.append(AgentMessage(from_agent, to_agent, content, msg_type))

    def run_single(self, agent_key: str, user_message: str, memory_context: str = "") -> str:
        handler = self.handlers.get(agent_key)
        if not handler:
            return f"Agent `{agent_key}` not available."
        # Inject memory context if present
        enriched = user_message
        if memory_context:
            enriched = f"[Session context]\n{memory_context}\n\n[User request]\n{user_message}"
        result = handler(enriched)
        self.send("orchestrator", agent_key, f"Delegated: {user_message[:80]}", "request")
        self.send(agent_key, "orchestrator", result[:120], "result")
        return result

    def run_collaborative(
        self,
        pattern: dict,
        user_message: str,
        memory_context: str = "",
    ) -> str:
        """
        Run multiple agents in sequence and combine outputs.
        Each agent receives prior agent summary as context (agent communication).
        """
        agents = pattern["agents"]
        parts = []
        prior_summary = ""

        header = (
            f"**Collaborative workflow:** {pattern['description']}\n"
            f"**Agents involved:** " + " → ".join(
                AGENT_ROLES[a]["name"] for a in agents if a in AGENT_ROLES
            ) + "\n"
        )
        parts.append(header)

        for i, agent_key in enumerate(agents):
            role = AGENT_ROLES.get(agent_key, {})
            name = role.get("name", agent_key)

            # Build message for this agent including prior agent output
            agent_input = user_message
            if prior_summary:
                agent_input = (
                    f"{user_message}\n\n"
                    f"[Context from previous agent]\n{prior_summary}"
                )
                self.send(agents[i - 1], agent_key, prior_summary[:100], "context")

            if memory_context:
                agent_input = f"[Memory]\n{memory_context}\n\n{agent_input}"

            handler = self.handlers.get(agent_key)
            if not handler:
                continue

            result = handler(agent_input)
            self.send(agent_key, "coordinator", "completed step", "result")

            parts.append(f"### Step {i + 1}: {name}\n\n{result}")
            # Keep a short summary for the next agent
            prior_summary = result[:300].replace("\n", " ")

        parts.append(
            "\n---\n*Workflow complete. Agents coordinated via shared context and message log.*"
        )
        return "\n\n".join(parts)

    def get_message_log(self) -> str:
        if not self.message_log:
            return "No inter-agent messages yet."
        lines = [m.format() for m in self.message_log[-10:]]
        return "**Agent communication log:**\n" + "\n".join(f"- {l}" for l in lines)
