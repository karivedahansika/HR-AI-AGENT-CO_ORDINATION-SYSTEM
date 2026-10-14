from utils.helpers import format_agent_response


def handle(user_message: str) -> str:
    """
    HR Ops & Compliance Agent
    Handles policies, leave, benefits, compliance, and general HR operations.
    """
    msg = user_message.lower()

    # Leave related
    if any(k in msg for k in ["leave", "attendance", "maternity", "paternity", "sick", "casual", "privilege"]):
        content = """**Leave & Attendance Guidance**

**Common Leave Types (typical structure)**
- Casual / Sick Leave
- Privilege / Earned Leave
- Maternity Leave (usually 26 weeks in many regions)
- Paternity Leave
- Bereavement / Compassionate Leave
- Compensatory Off

**How I can help**
- Explain leave eligibility and process
- Check policy interpretation
- Draft leave approval / rejection communication
- Guide on leave balance queries

**Note:** Always refer to your company’s official leave policy for exact entitlements, as they vary by location and employment contract.

Which leave type or situation do you need clarity on?"""

    # Policy / Compliance
    elif any(k in msg for k in ["policy", "policies", "compliance", "handbook", "code of conduct", "guideline"]):
        content = """**Policy & Compliance Support**

I can help you with:

- Interpreting HR policies in plain language  
- Checking if a situation complies with policy  
- Drafting policy communication or FAQs  
- Flagging potential compliance risks  
- Suggesting updates when policies feel outdated  

**Common Policy Areas**
- Code of Conduct  
- Leave & Attendance  
- Work from Home / Hybrid  
- Prevention of Harassment  
- Data Privacy & Confidentiality  
- Performance & Disciplinary process  

Share the policy topic or the specific situation, and I’ll give clear guidance."""

    # Benefits
    elif any(k in msg for k in ["benefit", "benefits", "insurance", "medical", "pf", "gratuity", "perks"]):
        content = """**Benefits Support**

I can help explain and guide on:

- Health insurance & medical claims process  
- Retirement benefits (PF, gratuity, etc.)  
- Wellness programs  
- Employee assistance programs  
- Other perks (meal cards, learning allowances, etc.)

**Typical Flow for Benefits Queries**
1. Understand the employee’s question  
2. Map to relevant benefit policy  
3. Provide clear next steps or required forms  
4. Escalate to benefits vendor / finance if needed  

What benefit-related question do you have?"""

    # Employee Relations
    elif any(k in msg for k in ["grievance", "complaint", "employee relations", "conflict", "disciplinary"]):
        content = """**Employee Relations Guidance**

**Recommended Approach**
1. Listen carefully and document facts  
2. Stay neutral and confidential  
3. Check relevant policies  
4. Involve the right stakeholders (manager, legal if needed)  
5. Take timely, fair action  
6. Follow up

**I can help you with**
- Structuring investigation steps  
- Drafting neutral communication  
- Checking policy alignment  
- Preparing documentation

Please share the nature of the situation (without sensitive personal details if possible) so I can guide you appropriately."""

    else:
        content = """I'm the **HR Ops & Compliance Agent**. I support:

- Leave & attendance questions  
- HR policy interpretation  
- Benefits guidance  
- Compliance checks  
- Employee relations support  

How can I help you today?"""

    return format_agent_response("HR Ops & Compliance Agent", content)
