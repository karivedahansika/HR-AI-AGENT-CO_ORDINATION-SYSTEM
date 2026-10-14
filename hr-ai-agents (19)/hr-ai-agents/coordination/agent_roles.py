"""
Defined business roles for each specialized agent.
"""

AGENT_ROLES = {
    "talent_acquisition": {
        "name": "Talent Acquisition Agent",
        "role": "Recruitment specialist",
        "responsibilities": [
            "Job descriptions",
            "Resume screening",
            "Interview questions",
            "Offer process support",
        ],
        "can_collaborate_with": ["employee_lifecycle", "hr_ops_compliance"],
        "tools": ["resume_screener", "interview_questions"],
    },
    "employee_lifecycle": {
        "name": "Employee Lifecycle Agent",
        "role": "Employee journey specialist",
        "responsibilities": [
            "Onboarding plans",
            "Offboarding",
            "Transfers and role changes",
            "Leave balance during transitions",
        ],
        "can_collaborate_with": ["talent_acquisition", "hr_ops_compliance", "performance_growth"],
        "tools": ["onboarding_generator", "leave_balance"],
    },
    "performance_growth": {
        "name": "Performance & Growth Agent",
        "role": "Performance and development specialist",
        "responsibilities": [
            "Performance reviews",
            "Goal / OKR setting",
            "Feedback frameworks",
            "Promotion discussion support",
        ],
        "can_collaborate_with": ["employee_lifecycle", "hr_ops_compliance"],
        "tools": ["interview_questions"],
    },
    "hr_ops_compliance": {
        "name": "HR Ops & Compliance Agent",
        "role": "Operations and policy specialist",
        "responsibilities": [
            "Policy interpretation",
            "Leave and attendance",
            "Benefits guidance",
            "Compliance checks",
        ],
        "can_collaborate_with": ["talent_acquisition", "employee_lifecycle", "performance_growth"],
        "tools": ["policy_checker", "leave_balance"],
    },
}


def get_role_card(agent_key: str) -> str:
    r = AGENT_ROLES.get(agent_key)
    if not r:
        return ""
    lines = [
        f"**{r['name']}** — {r['role']}",
        "Responsibilities: " + "; ".join(r["responsibilities"]),
    ]
    return "\n".join(lines)
