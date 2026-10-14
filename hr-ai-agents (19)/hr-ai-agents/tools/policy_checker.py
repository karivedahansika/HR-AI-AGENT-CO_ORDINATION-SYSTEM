"""Policy Checker Tool – quick compliance / policy answers."""

POLICIES = {
    "maternity": "Maternity leave: 26 weeks paid. Can start up to 8 weeks before expected delivery. Medical certificate required.",
    "paternity": "Paternity leave: 15 days paid, to be taken within 3 months of child's birth.",
    "notice": "Notice period: 30 days during probation, 60 days after confirmation (90 days for senior roles).",
    "probation": "Probation: 6 months. Reviews at 3 and 6 months. Confirmation based on performance and training completion.",
    "wfh": "Work from home: up to 2 days/week with manager approval. Core hours 11 AM – 4 PM.",
    "gratuity": "Gratuity: eligible after 5 years continuous service. Formula: (Last basic × 15 × years) / 26.",
}

def check_policy(query: str) -> str:
    q = query.lower()
    matched = []
    for key, text in POLICIES.items():
        if key in q or any(w in q for w in key.split()):
            matched.append(text)
    if "leave" in q and not matched:
        matched.append(POLICIES["maternity"])
        matched.append(POLICIES["paternity"])

    if not matched:
        return """**Policy Checker**

No exact match. You can check:
- Maternity / Paternity leave
- Notice period
- Probation
- Work from home
- Gratuity

Example: "Check maternity policy" or "What is notice period?"
"""
    out = "**Policy Checker Result**\n\n"
    for i, m in enumerate(matched, 1):
        out += f"{i}. {m}\n\n"
    return out.strip()
