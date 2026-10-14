"""
Orchestrator: routes to agents/tools, coordinates multi-agent workflows,
and uses short-term + long-term memory.
"""

import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.talent_acquisition import handle as ta_handle
from agents.employee_lifecycle import handle as lifecycle_handle
from agents.performance_growth import handle as performance_handle
from agents.hr_ops_compliance import handle as ops_handle
from utils.helpers import detect_intent
from tools.tool_router import use_tool
from memory.short_term import get_short_term
from memory.long_term import get_long_term
from coordination.coordinator import Coordinator
from workflows.orchestrator_engine import WorkflowEngine, get_metrics
from coordination.agent_roles import AGENT_ROLES
from foundation.langchain_setup import langchain_status
from prompts.templates import WORKFLOWS


AGENT_HANDLERS = {
    "talent_acquisition": ta_handle,
    "employee_lifecycle": lifecycle_handle,
    "performance_growth": performance_handle,
    "hr_ops_compliance": ops_handle,
}

coordinator = Coordinator(AGENT_HANDLERS)
workflow_engine = WorkflowEngine(AGENT_HANDLERS)


def is_hr_or_tool_query(message: str) -> bool:
    msg = message.lower()
    keywords = [
        "job description", "jd", "resume", "cv", "candidate", "interview", "hire", "recruit",
        "offer", "onboard", "offboard", "exit", "leave", "policy", "maternity", "paternity",
        "performance", "review", "goal", "okr", "employee", "screen resume", "shortlist",
        "interview question", "leave balance", "check policy", "onboarding plan",
        "notice period", "probation", "gratuity", "wfh", "work from home", "checklist",
        "promotion", "new hire", "new joiner", "resign",
    ]
    return any(k in msg for k in keywords)


def is_memory_command(message: str) -> str | None:
    """Detect explicit memory commands. Returns command type or None."""
    msg = message.lower().strip()
    if msg.startswith("remember ") or msg.startswith("save fact "):
        return "remember"
    if msg.startswith("recall ") or msg.startswith("what do you know about "):
        return "recall"
    if "memory log" in msg or "agent log" in msg or "show coordination" in msg:
        return "log"
    if "clear memory" in msg or "forget session" in msg:
        return "clear_short"
    return None


def handle_memory_command(cmd: str, message: str) -> str:
    stm = get_short_term()
    ltm = get_long_term()
    msg = message.strip()

    if cmd == "remember":
        # remember X is Y  OR  remember: key = value
        body = re.sub(r"^(remember|save fact)\s+", "", msg, flags=re.I).strip()
        if " is " in body.lower():
            parts = re.split(r"\s+is\s+", body, maxsplit=1, flags=re.I)
            key, value = parts[0].strip(), parts[1].strip()
        elif "=" in body:
            key, value = [p.strip() for p in body.split("=", 1)]
        else:
            key, value = "note", body
        ltm.remember_fact(key, value)
        stm.set_fact(key, value)
        return f"**Long-term memory updated**\n\nSaved: **{key}** = {value}"

    if cmd == "recall":
        body = re.sub(r"^(recall|what do you know about)\s+", "", msg, flags=re.I).strip()
        # try fact + employee notes + search
        fact = ltm.get_fact(body)
        notes = ltm.get_employee_notes(body)
        search = ltm.search(body)
        lines = ["**Memory recall**\n"]
        if fact:
            lines.append(f"- Fact: {fact}")
        if notes:
            lines.append("- Notes: " + "; ".join(notes))
        if search and "No matching" not in search:
            lines.append(search)
        if len(lines) == 1:
            lines.append("Nothing found in long-term memory for that query.")
        # also short-term
        ctx = stm.get_context_summary()
        if ctx:
            lines.append("\n**Recent session context:**\n" + ctx)
        return "\n".join(lines)

    if cmd == "log":
        return coordinator.get_message_log()

    if cmd == "clear_short":
        stm.clear()
        return "Short-term (session) memory cleared."

    return "Unknown memory command."


def general_response(message: str) -> str:
    msg = message.lower().strip()
    if re.search(r"^(hi|hello|hey)\b", msg):
        return "Hello! How can I help you today?"
    if "how are you" in msg:
        return "I'm doing well, thank you! How can I help with HR today?"
    if "who are you" in msg or "what can you do" in msg:
        roles = "\n".join(
            f"- **{r['name']}**: {r['role']}" for r in AGENT_ROLES.values()
        )
        return f"""I'm your HR Assistant with coordinated agents and memory.

**Specialized agents:**
{roles}

**Tools:** Resume Screener · Interview Questions · Leave Balance · Policy Checker · Onboarding Generator

**Memory:**
- Short-term: this conversation
- Long-term: say `remember company holiday is Diwali` or `recall Diwali`

**Collaboration:** try "hire and onboard a new engineer" to run multiple agents together.

**Foundation:** LangChain-ready prompts + connectors (mode: {langchain_status()['mode']})
**Workflows:** {', '.join(WORKFLOWS.keys())}"""
    if "thank" in msg:
        return "You're welcome!"
    if "bye" in msg:
        return "Goodbye! Have a great day."
    return f"""I noted: "{message}"

I can help with HR agents, tools, and memory.
Try a recruitment, onboarding, policy, or performance question — or a multi-step request like "promotion process for a team lead"."""


def process_message(user_message: str, conversation_history: list | None = None) -> str:
    """
    Main entry:
    1. Memory commands
    2. Tools
    3. Collaborative multi-agent workflows
    4. Single-agent routing
    5. General chat
    """
    if not user_message or not user_message.strip():
        return "Please type a message so I can help you."

    stm = get_short_term()
    ltm = get_long_term()

    # Sync optional history from UI into short-term
    if conversation_history:
        stm.clear()
        for m in conversation_history[-12:]:
            stm.add(m.get("role", "user"), m.get("content", ""))

    stm.add("user", user_message)
    memory_context = stm.get_context_summary()

    # 1) Explicit memory commands
    mem_cmd = is_memory_command(user_message)
    if mem_cmd:
        result = handle_memory_command(mem_cmd, user_message)
        stm.add("assistant", result)
        return result

    # 2) Tools
    tool_result = use_tool(user_message)
    if tool_result:
        try:
            from workflows.orchestrator_engine import _METRICS
            _METRICS["tool_calls"] = _METRICS.get("tool_calls", 0) + 1
        except Exception:
            pass
        ltm.log_decision("tool", user_message[:80], tool_result[:80])
        stm.add("assistant", tool_result)
        return tool_result

    # 3) Collaborative workflow
    if is_hr_or_tool_query(user_message):
        # Complex workflow automation (Milestone 4)
        wf = workflow_engine.detect(user_message)
        if wf:
            result = workflow_engine.run(wf, user_message, memory_context)
            ltm.log_decision("workflow_engine", wf.get("name", "workflow"), "workflow completed")
            stm.add("assistant", result)
            return result

        pattern = coordinator.detect_collaboration(user_message)
        if pattern:
            result = coordinator.run_collaborative(pattern, user_message, memory_context)
            ltm.log_decision("coordinator", pattern["name"], "collaborative workflow completed")
            stm.add("assistant", result)
            return result

        # 4) Single agent
        intents = detect_intent(user_message)
        if not intents:
            intents = ["hr_ops_compliance"]

        # Prefer non-ops if multiple
        agent_key = intents[0]
        for intent in intents:
            if intent != "hr_ops_compliance":
                agent_key = intent
                break

        # Enrich with long-term employee notes if a name appears
        for word in user_message.split():
            if len(word) > 3:
                notes = ltm.get_employee_notes(word)
                if notes:
                    memory_context += f"\nKnown notes on {word}: " + "; ".join(notes)

        result = coordinator.run_single(agent_key, user_message, memory_context)
        agent_name = AGENT_ROLES.get(agent_key, {}).get("name", agent_key)
        ltm.log_decision(agent_name, user_message[:80], result[:80])
        stm.add("assistant", result)
        return result

    # 5) General
    result = general_response(user_message)
    stm.add("assistant", result)
    return result
