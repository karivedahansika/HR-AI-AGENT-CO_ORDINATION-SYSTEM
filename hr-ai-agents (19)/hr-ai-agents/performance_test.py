"""Performance testing and optimization checks (Milestone 4)."""

import time
import statistics
from orchestrator import process_message
from workflows.orchestrator_engine import get_metrics


QUERIES = [
    "hi",
    "Write a job description for Data Analyst",
    "Screen resume for Data Analyst",
    "Check maternity policy",
    "Leave balance for Priya Sharma",
    "hire and onboard a new software engineer",
    "remember perf_test_key is ok",
    "recall perf_test_key",
]


def run_performance_test(rounds: int = 3):
    print("=" * 60)
    print("PERFORMANCE TEST – HR AI Agents")
    print("=" * 60)
    all_durations = []
    per_query = {q: [] for q in QUERIES}

    for r in range(rounds):
        print(f"\nRound {r + 1}/{rounds}")
        for q in QUERIES:
            t0 = time.perf_counter()
            try:
                process_message(q)
                ok = True
            except Exception as e:
                ok = False
                print(f"  FAIL {q[:40]}: {e}")
            ms = (time.perf_counter() - t0) * 1000
            all_durations.append(ms)
            per_query[q].append(ms)
            status = "OK" if ok else "ERR"
            print(f"  [{status}] {ms:7.1f} ms  |  {q[:50]}")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Requests:     {len(all_durations)}")
    print(f"Mean (ms):    {statistics.mean(all_durations):.1f}")
    print(f"Median (ms):  {statistics.median(all_durations):.1f}")
    print(f"Max (ms):     {max(all_durations):.1f}")
    print(f"Min (ms):     {min(all_durations):.1f}")
    if len(all_durations) > 1:
        print(f"Stdev (ms):   {statistics.stdev(all_durations):.1f}")

    print("\nPer-query averages:")
    for q, times in per_query.items():
        print(f"  {statistics.mean(times):7.1f} ms  |  {q[:50]}")

    print("\nWorkflow metrics:", get_metrics())
    print("\nOptimization notes:")
    print("- Rule-based handlers are fast (<50ms typical)")
    print("- Multi-agent workflows take longer (multiple steps)")
    print("- Enable caching for repeated policy/leave lookups in production")
    print("=" * 60)


if __name__ == "__main__":
    run_performance_test()
