from agents.talent_acquisition import handle as ta_handle
from agents.employee_lifecycle import handle as lifecycle_handle
from agents.performance_growth import handle as performance_handle
from agents.hr_ops_compliance import handle as ops_handle
from utils.helpers import detect_intent


AGENT_MAP = {
    "talent_acquisition": {
        "name": "Talent Acquisition Agent",
        "handler": ta_handle
    },
    "employee_lifecycle": {
        "name": "Employee Lifecycle Agent",
        "handler": lifecycle_handle
    },
    "performance_growth": {
        "name": "Performance & Growth Agent",
        "handler": performance_handle
    },
    "hr_ops_compliance": {
        "name": "HR Ops & Compliance Agent",
        "handler": ops_handle
    }
}


def process_message(user_message: str) -> str:
    """
    Main orchestrator function.
    Detects intent → calls relevant agent(s) → returns combined response.
    """
    if not user_message or not user_message.strip():
        return "Please type a message so I can help you."

    intents = detect_intent(user_message)

    responses = []
    for intent in intents:
        agent = AGENT_MAP.get(intent)
        if agent:
            response = agent["handler"](user_message)
            responses.append(response)

    if not responses:
        # Fallback
        return AGENT_MAP["hr_ops_compliance"]["handler"](user_message)

    # If multiple agents matched, join them cleanly
    if len(responses) == 1:
        return responses[0]

    combined = "I found multiple relevant areas. Here's help from the specialists:\n\n"
    combined += "\n\n---\n\n".join(responses)
    return combined
