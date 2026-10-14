from utils.helpers import format_agent_response


def handle(user_message: str) -> str:
    """
    Performance & Growth Agent
    Handles reviews, goals, feedback, skill gaps, and development.
    """
    msg = user_message.lower()

    # Performance Reviews
    if any(k in msg for k in ["performance", "review", "appraisal", "rating"]):
        content = """**Performance Review Support**

I can help you with:

**1. Review Preparation**
- Key discussion points based on goals
- Strengths & development areas framework
- Rating calibration guidance

**2. Feedback Structure (Recommended)**
- Specific examples (Situation → Behavior → Impact)
- Balanced view (what went well + what to improve)
- Forward-looking development actions

**3. Common Rating Scale Guidance**
- Exceeds Expectations
- Meets Expectations
- Needs Improvement
- Unsatisfactory

Would you like me to:
- Draft review talking points for a specific employee?
- Create a 360 feedback summary template?
- Help set goals for the next cycle?"""

    # Goals / OKRs
    elif any(k in msg for k in ["goal", "okr", "kpi", "objective"]):
        content = """**Goal Setting Guidance (OKR / KPI style)**

**Good Goal Characteristics**
- Specific & measurable
- Aligned to team/company objectives
- Time-bound
- Challenging but achievable

**Example Format**
- **Objective:** Improve customer onboarding experience  
- **Key Results:**
  - Reduce average onboarding time from 14 to 8 days
  - Achieve 90%+ onboarding satisfaction score
  - Complete documentation of all onboarding playbooks

I can help you write goals for individuals or teams.  
Just share the role or focus area."""

    # Feedback & Development
    elif any(k in msg for k in ["feedback", "development", "skill gap", "learning", "training", "growth"]):
        content = """**Feedback & Development Support**

**Giving Effective Feedback**
- Be timely and specific
- Focus on behavior, not personality
- Balance recognition and improvement areas
- End with clear next steps

**Skill Gap Analysis Approach**
1. List required skills for the role
2. Assess current proficiency
3. Identify priority gaps
4. Recommend learning actions (courses, projects, mentoring)

**Development Plan Template**
- Skill to develop
- Why it matters
- Learning activities
- Timeline & success measure
- Support needed from manager

Tell me the employee’s role or the skill area you want to focus on."""

    else:
        content = """I'm the **Performance & Growth Agent**. I can help with:

- Performance review preparation & summaries  
- Goal / OKR setting  
- Constructive feedback frameworks  
- Skill gap analysis  
- Individual development plans  

What would you like to work on?"""

    return format_agent_response("Performance & Growth Agent", content)
