from utils.helpers import format_agent_response


def handle(user_message: str) -> str:
    """
    Talent Acquisition Agent
    Handles job descriptions, screening, interviews, offers, and pipeline.
    """
    msg = user_message.lower()

    # Job Description
    if any(k in msg for k in ["job description", "jd", "job posting", "write a job"]):
        content = """Here's a professional job description template:

**Job Title:** Senior Data Analyst  
**Location:** [City / Remote]  
**Employment Type:** Full-time  

**About the Role**  
We are looking for a Senior Data Analyst to turn complex data into clear insights that drive business decisions.

**Key Responsibilities**
- Analyze large datasets and build dashboards
- Partner with product and business teams
- Design and maintain data models
- Present findings to stakeholders
- Mentor junior analysts

**Requirements**
- 5+ years of experience in data analysis
- Strong SQL, Python/R, and visualization tools (Tableau/Power BI)
- Excellent communication skills
- Bachelor’s degree in a quantitative field

**Nice to Have**
- Experience with cloud platforms (AWS/GCP/Azure)
- Knowledge of statistical modeling

Would you like me to customize this for a different role or add specific requirements?"""

    # Resume Screening
    elif any(k in msg for k in ["resume", "cv", "screen", "shortlist", "candidate"]):
        content = """**Resume Screening Guidance**

I can help you evaluate candidates. Please share the resume text or key points, and I will:

1. Match skills against the job requirements
2. Flag strengths and potential gaps
3. Suggest interview focus areas
4. Give a recommended rating (Strong / Moderate / Weak fit)

**Quick Screening Checklist**
- Relevant experience years
- Core technical skills present
- Career progression
- Red flags (job hopping, unexplained gaps)
- Culture / soft skills indicators

Paste the resume or tell me the role + candidate highlights to proceed."""

    # Interview Scheduling / Process
    elif any(k in msg for k in ["interview", "schedule", "round"]):
        content = """**Interview Process Recommendation**

Suggested structure for most mid-senior roles:

1. **Recruiter Screen** (20–30 min) – Culture, motivation, logistics  
2. **Technical / Skills Interview** (45–60 min)  
3. **Hiring Manager Interview** (45 min)  
4. **Team / Culture Fit** (30 min)  
5. **Final / Leadership round** (if needed)

I can also draft interview questions, scorecards, or rejection/offer emails.

What stage are you currently at?"""

    # Offer Letter
    elif any(k in msg for k in ["offer", "offer letter", "compensation"]):
        content = """**Offer Letter Draft Support**

I can help you create a clear, professional offer letter. Typical sections:

- Position title & reporting manager  
- Start date & location  
- Compensation (base + variable + equity if any)  
- Benefits summary  
- Probation period  
- Confidentiality & other standard clauses  

Please share:
- Role title
- Candidate name
- CTC / compensation details
- Start date

I’ll generate a ready-to-edit draft."""

    else:
        content = """I'm the **Talent Acquisition Agent**. I can help you with:

- Writing or improving job descriptions  
- Screening resumes and shortlisting candidates  
- Designing interview processes & questions  
- Drafting offer letters  
- Tracking hiring pipeline health  

What would you like to work on today?"""

    return format_agent_response("Talent Acquisition Agent", content)
