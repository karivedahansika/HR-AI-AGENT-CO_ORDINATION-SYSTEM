"""Interview Question Generator Tool."""

def generate_questions(query: str) -> str:
    q = query.lower()
    role = "General"
    if "data" in q or "analyst" in q:
        role = "Data Analyst"
    elif "engineer" in q or "developer" in q:
        role = "Software Engineer"
    elif "hr" in q:
        role = "HR"
    elif "manager" in q:
        role = "Manager"
    elif "sales" in q:
        role = "Sales"

    return f"""**Interview Questions – {role}**

**1. Screening (Recruiter)**
- Walk me through your relevant experience for this role.
- Why are you interested in this position and our company?
- What are your salary expectations and notice period?

**2. Technical / Role-specific**
- Describe a challenging project you owned end-to-end.
- How do you prioritise work when deadlines conflict?
- Share an example of a mistake you made and what you learned.

**3. Behavioural**
- Tell me about a time you handled conflict in a team.
- Give an example of when you went beyond your job scope.
- How do you handle feedback from managers or peers?

**4. Closing**
- Do you have questions for us?
- Are you interviewing with other companies?

*Ask for a specific role to get more tailored questions.*
"""
