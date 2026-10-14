from utils.helpers import format_agent_response
from tools.resume_screener import screen_resume
from tools.interview_questions import generate_questions


def handle(user_message: str) -> str:
    msg = user_message.lower()

    if any(k in msg for k in ["screen resume", "resume screen", "score resume", "candidate fit", "shortlist"]):
        return format_agent_response("Talent Acquisition Agent + Resume Screener", screen_resume(user_message))

    if any(k in msg for k in ["interview question", "generate interview", "interview questions"]):
        return format_agent_response("Talent Acquisition Agent + Interview Questions", generate_questions(user_message))

    if any(k in msg for k in ["job description", "jd", "job posting", "write a job"]):
        content = """Here's a professional job description template:

**Job Title:** Senior Data Analyst  
**Location:** [City / Remote]  
**Employment Type:** Full-time  

**About the Role**  
Turn complex data into clear insights that drive business decisions.

**Key Responsibilities**
- Analyze datasets and build dashboards
- Partner with product and business teams
- Design and maintain data models
- Present findings to stakeholders

**Requirements**
- 5+ years in data analysis
- Strong SQL, Python/R, Tableau/Power BI
- Excellent communication skills

I can also **screen resumes** or **generate interview questions** for this role."""

    elif any(k in msg for k in ["resume", "cv", "candidate", "screening"]):
        content = """I can screen resumes for you.

Try:
- "Screen resume for Data Analyst"
- Or paste candidate highlights and ask for a fit score

I also generate interview questions — say "Generate interview questions for Software Engineer"."""

    elif any(k in msg for k in ["interview", "offer"]):
        content = """I can help with interviews and offers.

**Try:**
- Generate interview questions for [role]
- Write a job description for [role]
- Screen resume for [role]"""

    else:
        content = """I'm the **Talent Acquisition Agent**.

**Tools I use:**
- Resume Screener
- Interview Question Generator

**Try:**
- Write a job description for Data Analyst
- Screen resume for Software Engineer
- Generate interview questions for HR Manager"""

    return format_agent_response("Talent Acquisition Agent", content)
