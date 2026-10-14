"""Validate collaborative workflows, memory, and agent coordination."""

from orchestrator import process_message, coordinator
from memory.short_term import get_short_term
from memory.long_term import get_long_term
from coordination.agent_roles import AGENT_ROLES


def run():
    print("=" * 60)
    print("1. AGENT ROLES")
    print("=" * 60)
    for k, r in AGENT_ROLES.items():
        print(f"  - {r['name']}: {r['role']}")
        print(f"    Collaborates with: {', '.join(r['can_collaborate_with'])}")

    print("\n" + "=" * 60)
    print("2. SHORT-TERM MEMORY")
    print("=" * 60)
    stm = get_short_term()
    stm.clear()
    stm.add("user", "I need to hire a data analyst")
    stm.add("assistant", "I can help with JD and screening.")
    print(stm.get_context_summary())

    print("\n" + "=" * 60)
    print("3. LONG-TERM MEMORY")
    print("=" * 60)
    ltm = get_long_term()
    ltm.remember_fact("company_holiday", "Diwali week is company holiday")
    ltm.add_employee_note("Priya Sharma", "Strong performer in Q2 reviews")
    print("Fact:", ltm.get_fact("company_holiday"))
    print("Notes:", ltm.get_employee_notes("Priya Sharma"))
    print(ltm.search("Diwali"))

    print("\n" + "=" * 60)
    print("4. MEMORY COMMANDS VIA ORCHESTRATOR")
    print("=" * 60)
    print(process_message("remember notice period is 60 days")[:120])
    print(process_message("recall notice period")[:120])

    print("\n" + "=" * 60)
    print("5. SINGLE AGENT")
    print("=" * 60)
    r = process_message("Write a job description for Data Analyst")
    print(r[:150])

    print("\n" + "=" * 60)
    print("6. COLLABORATIVE WORKFLOW")
    print("=" * 60)
    r = process_message("hire and onboard a new software engineer")
    print(r[:400])
    print("...")
    print("\nMessage log sample:")
    print(coordinator.get_message_log()[:300])

    print("\n" + "=" * 60)
    print("VALIDATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    run()
