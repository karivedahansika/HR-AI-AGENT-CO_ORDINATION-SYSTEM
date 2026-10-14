"""Leave Balance Checker Tool."""

SAMPLE = {
    "priya sharma": {"casual": 6, "sick": 8, "privilege": 12, "used_casual": 2, "used_sick": 1, "used_privilege": 4},
    "amit patel": {"casual": 6, "sick": 8, "privilege": 15, "used_casual": 3, "used_sick": 0, "used_privilege": 7},
    "neha gupta": {"casual": 6, "sick": 8, "privilege": 18, "used_casual": 1, "used_sick": 2, "used_privilege": 5},
    "default": {"casual": 6, "sick": 8, "privilege": 12, "used_casual": 0, "used_sick": 0, "used_privilege": 0},
}

def check_leave(query: str) -> str:
    q = query.lower()
    data = SAMPLE["default"]
    name = "Employee"
    for n, d in SAMPLE.items():
        if n != "default" and n in q:
            data = d
            name = n.title()
            break

    return f"""**Leave Balance – {name}**

| Leave Type | Entitled | Used | Balance |
|------------|-----------|------|---------|
| Casual Leave | {data['casual']} | {data['used_casual']} | **{data['casual']-data['used_casual']}** |
| Sick Leave | {data['sick']} | {data['used_sick']} | **{data['sick']-data['used_sick']}** |
| Privilege / Earned | {data['privilege']} | {data['used_privilege']} | **{data['privilege']-data['used_privilege']}** |

**Total remaining:** {data['casual']-data['used_casual'] + data['sick']-data['used_sick'] + data['privilege']-data['used_privilege']} days

*Try: "Leave balance for Priya Sharma"*
"""
