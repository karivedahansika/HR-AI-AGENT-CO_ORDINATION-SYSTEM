from utils.helpers import format_agent_response
from tools.interview_questions import generate_questions


def handle(user_message: str) -> str:
    msg = user_message.lower()

    if any(k in msg for k in ["interview question", "generate interview"]):
        return format_agent_response("Performance & Growth Agent + Interview Questions", generate_questions(user_message))

    if any(k in msg for k in ["performance", "review", "appraisal", "rating"]):
        content = """**Performance Review Support**

1. Use specific examples (Situation → Behavior → Impact)
2. Balance strengths and development areas
3. Agree on clear next steps

**Rating scale:** 5 Outstanding · 4 Exceeds · 3 Meets · 2 Needs Improvement · 1 Unsatisfactory

I can also help set goals or generate role-based discussion questions."""

    elif any(k in msg for k in ["goal", "okr", "kpi"]):
        content = """**Goal setting tip**

- Specific and measurable
- Aligned to team objectives
- Time-bound

Example: Reduce onboarding time from 14 to 8 days by end of Q2."""

    else:
        content = """I'm the **Performance & Growth Agent**.

**Try:**
- Help me with performance review
- Set goals for a team lead
- Generate interview questions for promotion discussion"""

    return format_agent_response("Performance & Growth Agent", content)
