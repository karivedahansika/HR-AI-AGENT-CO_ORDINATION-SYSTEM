"""
Prompt templates and interaction workflows for HR agents.
Used as structured prompts (LangChain-compatible message format).
"""

from typing import List, Dict

# LangChain-style chat messages: role + content
SYSTEM_PROMPTS = {
    "talent_acquisition": (
        "You are the Talent Acquisition Agent for an enterprise HR system. "
        "You help with job descriptions, resume screening, interview questions, and offers. "
        "Be professional, structured, and actionable."
    ),
    "employee_lifecycle": (
        "You are the Employee Lifecycle Agent. "
        "You handle onboarding, offboarding, transfers, and leave during transitions. "
        "Provide clear checklists and next steps."
    ),
    "performance_growth": (
        "You are the Performance & Growth Agent. "
        "You support performance reviews, goals/OKRs, feedback, and development plans. "
        "Be constructive and specific."
    ),
    "hr_ops_compliance": (
        "You are the HR Ops & Compliance Agent. "
        "You explain policies, leave, benefits, and compliance. "
        "Be accurate and cite policy areas clearly."
    ),
    "orchestrator": (
        "You are the HR Assistant orchestrator. "
        "Route user requests to the right specialist agent or tool. "
        "For complex requests, coordinate multiple agents."
    ),
}


def build_agent_prompt(agent_key: str, user_message: str, context: str = "") -> List[Dict[str, str]]:
    """Build a prompt template workflow: system + optional context + user."""
    system = SYSTEM_PROMPTS.get(agent_key, SYSTEM_PROMPTS["orchestrator"])
    messages = [{"role": "system", "content": system}]
    if context:
        messages.append({
            "role": "system",
            "content": f"Relevant context from memory/previous agents:\n{context}",
        })
    messages.append({"role": "user", "content": user_message})
    return messages


def format_prompt_for_display(messages: List[Dict[str, str]]) -> str:
    """Readable form of the prompt workflow (for testing/debug)."""
    lines = []
    for m in messages:
        lines.append(f"[{m['role'].upper()}]\n{m['content']}")
    return "\n\n".join(lines)


# Interaction workflow names used by orchestrator
WORKFLOWS = {
    "single_agent": "Route to one specialist agent",
    "tool_first": "Try tools, then agents",
    "collaborative": "Multi-agent sequential coordination",
    "memory": "Remember / recall long-term facts",
}
