from utils.helpers import format_agent_response


def handle(user_message: str) -> str:
    """
    Employee Lifecycle Agent
    Handles onboarding, offboarding, transfers, and role changes.
    """
    msg = user_message.lower()

    # Onboarding
    if any(k in msg for k in ["onboard", "onboarding", "new joiner", "new hire", "joining", "welcome"]):
        content = """**New Joiner Onboarding Checklist**

**Pre-Joining (Before Day 1)**
- [ ] Send offer letter & collect acceptance
- [ ] Collect documents (ID, education, previous employment)
- [ ] Create email ID & system access requests
- [ ] Assign buddy / mentor
- [ ] Prepare workstation & welcome kit
- [ ] Share first-week agenda

**Day 1**
- [ ] Welcome meeting with HR & manager
- [ ] Complete joining formalities
- [ ] IT setup & tool access
- [ ] Company overview & culture session
- [ ] Introduce to team

**Week 1**
- [ ] Role expectation discussion
- [ ] Mandatory compliance trainings
- [ ] Benefits enrollment
- [ ] 1:1 with manager

**30 / 60 / 90 Day Checkpoints**
- Structured feedback conversations
- Goal setting for probation period

Would you like a customized checklist for a specific role (e.g. Engineer, Sales, Manager)?"""

    # Offboarding
    elif any(k in msg for k in ["offboard", "offboarding", "exit", "resignation", "leaving", "termination"]):
        content = """**Employee Offboarding Checklist**

**Immediate Actions**
- [ ] Acknowledge resignation / initiate exit process
- [ ] Confirm last working day
- [ ] Inform relevant stakeholders (manager, IT, finance, security)

**Knowledge & Access**
- [ ] Knowledge transfer plan with manager
- [ ] Revoke system access on last day
- [ ] Collect company assets (laptop, ID card, etc.)

**Documentation**
- [ ] Exit interview scheduling
- [ ] Full & final settlement calculation
- [ ] Experience / relieving letter preparation
- [ ] Update employee records in HRIS

**Post-Exit**
- [ ] Conduct exit interview summary
- [ ] Update org chart & succession notes
- [ ] Archive documents securely

I can also help draft exit interview questions or a knowledge transfer template. Just let me know."""

    # Role change / Transfer
    elif any(k in msg for k in ["transfer", "role change", "promotion", "internal move", "mobility"]):
        content = """**Internal Mobility / Role Change Support**

Recommended steps:

1. **Discussion** – Manager + employee alignment on new role
2. **HR Review** – Check eligibility, compensation impact, and policy
3. **Documentation** – Role change letter / transfer order
4. **Transition Plan** – Handover from current role + onboarding into new role
5. **System Updates** – Update HRIS, access rights, reporting structure
6. **Communication** – Inform team and stakeholders

I can help you create:
- Role change letter template
- Transition checklist
- Communication draft

What type of movement is this (promotion, lateral, location transfer)?"""

    else:
        content = """I'm the **Employee Lifecycle Agent**. I specialize in:

- Creating onboarding plans & checklists  
- Managing offboarding & exit processes  
- Supporting internal transfers and role changes  
- Ensuring smooth employee transitions  

Tell me what stage of the employee journey you need help with."""

    return format_agent_response("Employee Lifecycle Agent", content)
