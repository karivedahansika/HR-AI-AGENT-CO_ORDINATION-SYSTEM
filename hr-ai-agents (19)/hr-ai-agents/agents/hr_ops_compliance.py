from utils.helpers import format_agent_response
from tools.policy_checker import check_policy
from tools.leave_balance import check_leave


def handle(user_message: str) -> str:
    msg = user_message.lower()

    if any(k in msg for k in ["check policy", "policy", "maternity", "paternity", "notice period", "probation", "gratuity", "wfh", "work from home"]):
        return format_agent_response("HR Ops & Compliance Agent + Policy Checker", check_policy(user_message))

    if any(k in msg for k in ["leave balance", "check leave", "remaining leave", "leave for"]):
        return format_agent_response("HR Ops & Compliance Agent + Leave Balance", check_leave(user_message))

    if any(k in msg for k in ["leave", "attendance"]):
        content = """I can check leave balances and policies.

**Try:**
- Leave balance for Priya Sharma
- Check maternity policy
- What is notice period?"""

    else:
        content = """I'm the **HR Ops & Compliance Agent**.

**Tools I use:**
- Policy Checker
- Leave Balance Checker

**Try:**
- Check maternity policy
- Leave balance for Amit Patel
- What is the probation policy?"""

    return format_agent_response("HR Ops & Compliance Agent", content)
