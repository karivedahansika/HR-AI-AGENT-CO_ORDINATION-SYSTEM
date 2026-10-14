def format_agent_response(agent_name: str, content: str) -> str:
    """Format the final response with agent branding."""
    return f"**{agent_name}**\n\n{content}"


def detect_intent(user_message: str) -> list[str]:
    """
    Simple keyword-based intent detection.
    Returns a list of relevant agent keys.
    In production this would be replaced by an LLM classifier.
    """
    message = user_message.lower()

    intents = []

    # Talent Acquisition keywords
    ta_keywords = [
        "job description", "jd", "resume", "cv", "candidate", "screening",
        "interview", "hire", "hiring", "recruit", "offer letter", "shortlist",
        "pipeline", "talent", "job posting", "requisition"
    ]
    if any(k in message for k in ta_keywords):
        intents.append("talent_acquisition")

    # Employee Lifecycle keywords
    lifecycle_keywords = [
        "onboard", "onboarding", "new joiner", "new hire", "joining",
        "offboard", "offboarding", "exit", "resignation", "termination",
        "transfer", "role change", "promotion", "checklist", "welcome kit"
    ]
    if any(k in message for k in lifecycle_keywords):
        intents.append("employee_lifecycle")

    # Performance & Growth keywords
    performance_keywords = [
        "performance", "review", "appraisal", "feedback", "goal", "okr",
        "kpi", "rating", "development", "skill gap", "learning", "training",
        "promotion readiness", "360"
    ]
    if any(k in message for k in performance_keywords):
        intents.append("performance_growth")

    # HR Ops & Compliance keywords
    ops_keywords = [
        "leave", "attendance", "policy", "policies", "compliance", "benefit",
        "benefits", "payroll", "maternity", "paternity", "sick leave",
        "casual leave", "holiday", "grievance", "employee relations",
        "code of conduct", "handbook"
    ]
    if any(k in message for k in ops_keywords):
        intents.append("hr_ops_compliance")

    # Default fallback
    if not intents:
        intents.append("hr_ops_compliance")  # general HR questions

    return intents
