from utils.helpers import format_agent_response
from tools.onboarding_generator import generate_onboarding
from tools.leave_balance import check_leave


def handle(user_message: str) -> str:
    msg = user_message.lower()

    if any(k in msg for k in ["generate onboarding", "onboarding plan", "onboarding for", "create onboarding"]):
        return format_agent_response("Employee Lifecycle Agent + Onboarding Generator", generate_onboarding(user_message))

    if any(k in msg for k in ["leave balance", "check leave", "remaining leave"]):
        return format_agent_response("Employee Lifecycle Agent + Leave Balance", check_leave(user_message))

    if any(k in msg for k in ["onboard", "onboarding", "new joiner", "new hire", "joining"]):
        content = """I can generate a full onboarding plan.

**Try:** "Generate onboarding plan for Software Engineer"

Or ask about offboarding, transfers, or leave balance."""

    elif any(k in msg for k in ["offboard", "exit", "resignation", "leaving"]):
        content = """**Offboarding Checklist**
- Confirm last working day
- Knowledge transfer plan
- Revoke system access
- Collect assets
- Exit interview
- Experience / relieving letter

I can also check leave balance before final settlement."""

    else:
        content = """I'm the **Employee Lifecycle Agent**.

**Tools I use:**
- Onboarding Generator
- Leave Balance Checker

**Try:**
- Generate onboarding plan for Data Analyst
- Leave balance for Priya Sharma
- Create offboarding checklist"""

    return format_agent_response("Employee Lifecycle Agent", content)
