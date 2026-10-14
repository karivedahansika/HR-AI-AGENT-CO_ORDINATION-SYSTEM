"""Tool Router – intelligent tool selection + exception handling."""

from tools.resume_screener import screen_resume
from tools.interview_questions import generate_questions
from tools.leave_balance import check_leave
from tools.policy_checker import check_policy
from tools.onboarding_generator import generate_onboarding


def use_tool(user_message: str) -> str | None:
    """
    Select and invoke a tool. Returns tool output or None.
    All invocations are wrapped for exception handling.
    """
    msg = user_message.lower().strip()
    try:
        if any(k in msg for k in ["screen resume", "resume screen", "score resume", "candidate fit", "shortlist resume"]):
            return screen_resume(user_message)

        if any(k in msg for k in ["interview question", "generate interview", "interview questions", "questions for interview"]):
            return generate_questions(user_message)

        if any(k in msg for k in ["leave balance", "check leave", "remaining leave", "leave for"]):
            return check_leave(user_message)

        if any(k in msg for k in ["check policy", "policy check", "maternity policy", "notice period", "probation policy", "wfh policy", "gratuity"]):
            return check_policy(user_message)

        if any(k in msg for k in ["generate onboarding", "onboarding plan", "onboarding for", "create onboarding plan"]):
            return generate_onboarding(user_message)

        if "policy" in msg and any(k in msg for k in ["maternity", "paternity", "notice", "probation", "leave", "wfh", "work from home"]):
            return check_policy(user_message)

        return None
    except Exception as e:
        return f"**Tool Error**\n\nThe selected tool failed while running.\n\nDetails: `{str(e)}`\n\nPlease retry with a clearer request."
