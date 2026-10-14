"""Resume Screener – analyzes uploaded resume text and returns content-based ratings."""

import re
from typing import Dict, List, Tuple


ROLE_SKILLS = {
    "data analyst": [
        "sql", "python", "excel", "tableau", "power bi", "powerbi", "statistics",
        "analytics", "dashboard", "etl", "data analysis", "reporting", "pandas",
        "r ", "visualization", "metrics", "kpi",
    ],
    "software engineer": [
        "python", "java", "javascript", "react", "node", "sql", "git", "api",
        "aws", "docker", "kubernetes", "microservices", "backend", "frontend",
        "typescript", "c++", "spring", "rest",
    ],
    "hr": [
        "recruitment", "onboarding", "payroll", "employee relations", "hris",
        "talent", "performance", "compliance", "benefits", "interview",
        "hr", "human resources", "ats",
    ],
    "manager": [
        "leadership", "team", "stakeholder", "budget", "strategy", "kpi",
        "management", "planning", "delivery", "coaching", "p&l",
    ],
    "sales": [
        "sales", "crm", "negotiation", "pipeline", "quota", "client",
        "revenue", "b2b", "account", "target", "closing",
    ],
    "default": [
        "communication", "teamwork", "leadership", "project", "analysis",
        "problem solving", "collaboration", "microsoft", "excel", "presentation",
    ],
}


def _detect_role(query: str) -> str:
    q = query.lower()
    for role in ROLE_SKILLS:
        if role != "default" and role in q:
            return role
    if "developer" in q or "sde" in q or "programmer" in q:
        return "software engineer"
    if "analyst" in q:
        return "data analyst"
    return "default"


def _extract_resume_body(query: str) -> str:
    if "--- Uploaded file:" in query:
        try:
            part = query.split("--- Uploaded file:", 1)[1]
            if "--- End of file ---" in part:
                part = part.split("--- End of file ---", 1)[0]
            lines = part.strip().split("\n", 1)
            body = lines[1].strip() if len(lines) > 1 else lines[0].strip()
            return body
        except Exception:
            pass
    # fallback: strip common instruction prefixes
    return query


def _years_experience(text: str) -> float:
    t = text.lower()
    years = re.findall(r"(\d+)\s*\+?\s*(?:years?|yrs?)", t)
    if years:
        return max(float(y) for y in years)
    ranges = re.findall(r"(20\d{2})\s*[-–to]+\s*(20\d{2}|present|current)", t)
    total = 0
    for a, b in ranges:
        end = 2026 if b in ("present", "current") else int(b)
        total += max(0, end - int(a))
    return float(min(total, 40)) if total else 0.0


def _skill_match(text: str, skills: List[str]) -> Tuple[int, List[str], List[str]]:
    t = " " + text.lower() + " "
    found, missing = [], []
    for s in skills:
        # word-ish match
        if s.strip() in t:
            found.append(s.strip())
        else:
            missing.append(s.strip())
    ratio = len(found) / max(len(skills), 1)
    score = int(round(1 + ratio * 9))  # 1..10
    return max(1, min(10, score)), found, missing


def _progression_score(text: str) -> int:
    t = text.lower()
    score = 4
    if any(w in t for w in ["senior", "lead", "principal", "manager", "head", "director"]):
        score += 2
    if any(w in t for w in ["promoted", "promotion", "grew", "advanced", "awarded"]):
        score += 1
    jobs = len(re.findall(r"20\d{2}", t))
    if jobs >= 4:
        score += 2
    elif jobs >= 2:
        score += 1
    if len(text) > 800:
        score += 1
    return max(1, min(10, score))


def _communication_score(text: str) -> int:
    if text.startswith("[Image uploaded") or text.startswith("[PDF"):
        return 3
    if "No extractable text" in text or "scanned" in text.lower():
        return 2
    n = len(text)
    if n < 80:
        return 3
    if n < 300:
        return 5
    if n < 800:
        return 7
    if n < 2000:
        return 8
    return 9


def _exp_score(years: float) -> Tuple[int, str]:
    if years <= 0:
        return 4, "No clear years of experience found"
    if years < 2:
        return 5, f"~{years:.0f} year(s) — junior"
    if years < 5:
        return 7, f"~{years:.0f} years — mid-level"
    if years < 8:
        return 9, f"~{years:.0f} years — senior"
    return 10, f"~{years:.0f}+ years — highly experienced"


def _overall(scores: Dict[str, int]) -> float:
    w = {"experience": 0.25, "skills": 0.35, "progression": 0.20, "communication": 0.20}
    return round(sum(scores[k] * w[k] for k in w), 1)


def screen_resume(query: str) -> str:
    role = _detect_role(query)
    resume_text = _extract_resume_body(query).strip()
    skills = ROLE_SKILLS.get(role, ROLE_SKILLS["default"])

    # Guard: no real content
    if not resume_text or len(resume_text) < 30:
        return (
            "**Resume Screener**\n\n"
            "No resume content was found to analyze.\n\n"
            "**How to get a real rating:**\n"
            "1. Upload a **.txt** or **text-based PDF** resume in the sidebar\n"
            "2. Type: `Screen this resume for Data Analyst`\n"
            "3. Click **Send file to chat**\n\n"
            "Photo/scanned PDFs cannot be read without OCR."
        )

    thin = resume_text.startswith("[") and ("uploaded" in resume_text.lower() or "PDF" in resume_text)

    years = _years_experience(resume_text)
    exp_score, exp_note = _exp_score(years)
    skill_score, found, missing = _skill_match(resume_text, skills)
    if thin:
        skill_score = max(2, skill_score - 4)
        skill_note = "Limited text extracted — upload a text PDF or .txt for accuracy"
    else:
        skill_note = f"Matched: {', '.join(found[:8]) or 'none'}"
        if missing:
            skill_note += f" | Gaps: {', '.join(missing[:5])}"

    prog_score = _progression_score(resume_text)
    comm_score = _communication_score(resume_text)
    scores = {
        "experience": exp_score,
        "skills": skill_score,
        "progression": prog_score,
        "communication": comm_score,
    }
    overall = _overall(scores)

    if overall >= 8:
        verdict = "**Strong fit — recommend interview**"
    elif overall >= 6.5:
        verdict = "**Good fit — recommended for interview**"
    elif overall >= 5:
        verdict = "**Moderate fit — review before interview**"
    elif overall >= 3.5:
        verdict = "**Partial fit — needs stronger evidence**"
    else:
        verdict = "**Weak match — more information needed**"

    role_label = role.title() if role != "default" else "General"
    preview = resume_text[:320].replace("\n", " ").strip()
    if len(resume_text) > 320:
        preview += "..."

    lines = [
        "**Resume Screener Result** *(scanned from your file)*",
        "",
        f"**Target Role:** {role_label}",
        f"**Characters analyzed:** {len(resume_text)}",
        "",
        "| Criteria | Score | Notes |",
        "|----------|-------|-------|",
        f"| Relevant experience | {exp_score}/10 | {exp_note} |",
        f"| Skills match | {skill_score}/10 | {skill_note} |",
        f"| Career progression | {prog_score}/10 | Titles, dates, promotions in file |",
        f"| Communication / detail | {comm_score}/10 | Based on readable content length & clarity |",
        f"| **Overall Fit** | **{overall}/10** | {verdict} |",
        "",
        "**Interview focus:**",
    ]
    focus = missing[:3] if missing else ["Hands-on depth", "Problem-solving examples", "Team collaboration"]
    for m in focus:
        lines.append(f"- {m}")

    if preview and not preview.startswith("["):
        lines += ["", "**From your resume:**", f"> {preview}"]

    if thin:
        lines += [
            "",
            "_For accurate scores: upload a **text-based PDF** or **.txt** resume (not a photo)._",
        ]

    return "\n".join(lines)
