def format_agent_response(agent_name: str, content: str) -> str:
    """Format the final response with agent branding."""
    return f"**{agent_name}**\n\n{content}"


def detect_intent(user_message: str) -> list[str]:
    """
    Keyword-based intent detection.
    Routes both agent topics and tool requests to the right agent.
    """
    message = user_message.lower()
    intents = []

    # Talent Acquisition (includes offer email, offer letter, CTC calc)
    ta_keywords = [
        "job description", "jd", "resume", "cv", "candidate", "screening",
        "interview", "hire", "hiring", "recruit", "offer letter", "shortlist",
        "pipeline", "talent", "job posting", "requisition",
        "offer email", "rejection email", "interview email",
        "offer letter template", "screen resume", "interview question"
    ]
    if any(k in message for k in ta_keywords):
        intents.append("talent_acquisition")

    # Employee Lifecycle
    lifecycle_keywords = [
        "onboard", "onboarding", "new joiner", "new hire", "joining",
        "offboard", "offboarding", "exit", "resignation", "termination",
        "transfer", "role change", "promotion", "checklist", "welcome kit",
        "welcome email", "experience letter", "relieving letter", "onboarding plan", "leave balance"
    ]
    if any(k in message for k in lifecycle_keywords):
        intents.append("employee_lifecycle")

    # Performance & Growth
    performance_keywords = [
        "performance", "review", "appraisal", "feedback", "goal", "okr",
        "kpi", "rating", "development", "skill gap", "learning", "training",
        "promotion readiness", "360", "performance template"
    ]
    if any(k in message for k in performance_keywords):
        intents.append("performance_growth")

    # HR Ops & Compliance (policies, leave, search, database, general tools)
    ops_keywords = [
        "leave", "attendance", "policy", "policies", "compliance", "benefit",
        "benefits", "payroll", "maternity", "paternity", "sick leave",
        "casual leave", "holiday", "grievance", "employee relations",
        "code of conduct", "handbook", "search", "gratuity", "provident fund",
        "work from home", "notice period", "probation period",
        "find employee", "employees in", "how many employees", "on probation",
        "list files", "hr files", "available documents", "list available", "check policy", "policy check", "leave balance"
    ]
    if any(k in message for k in ops_keywords):
        intents.append("hr_ops_compliance")

    # Default fallback
    if not intents:
        intents.append("hr_ops_compliance")

    return intents
