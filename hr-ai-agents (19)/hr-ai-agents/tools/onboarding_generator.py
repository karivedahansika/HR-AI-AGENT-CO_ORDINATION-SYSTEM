"""Onboarding Plan Generator Tool."""

def generate_onboarding(query: str) -> str:
    q = query.lower()
    role = "New Joiner"
    for r in ["engineer", "analyst", "manager", "hr", "sales", "developer"]:
        if r in q:
            role = r.title()
            break

    return f"""**Onboarding Plan – {role}**

**Pre-Joining**
- [ ] Collect documents (ID, education, previous employment)
- [ ] Create email ID and system access
- [ ] Assign buddy / mentor
- [ ] Prepare workstation and welcome kit
- [ ] Share first-week agenda

**Day 1**
- [ ] HR welcome and joining formalities
- [ ] IT setup and tool access
- [ ] Meet manager and team
- [ ] Company overview session

**Week 1**
- [ ] Role expectations discussion
- [ ] Mandatory compliance trainings
- [ ] Benefits enrollment
- [ ] 1:1 with manager

**30 / 60 / 90 Days**
- [ ] Checkpoint feedback meetings
- [ ] Goal setting for probation
- [ ] Confirm access and training completion

*Ask for a specific role to customise further.*
"""
