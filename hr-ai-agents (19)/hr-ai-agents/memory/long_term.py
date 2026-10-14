"""
Long-term memory: persistent store for facts, past decisions, and preferences.
Stored as JSON on disk.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

DEFAULT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "long_term_memory.json",
)


class LongTermMemory:
    """File-backed long-term memory for HR facts and past interactions."""

    def __init__(self, path: str = DEFAULT_PATH):
        self.path = path
        self._data: Dict[str, Any] = {
            "facts": {},           # key-value durable facts
            "employee_notes": {},  # notes by employee name/id
            "decisions": [],       # past agent decisions / outcomes
            "preferences": {},     # user/HR preferences
        }
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self._data.update(loaded)
            except (json.JSONDecodeError, OSError):
                pass

    def _save(self) -> None:
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
        except OSError:
            # Disk/sync issues should not crash the app
            pass

    def remember_fact(self, key: str, value: str) -> None:
        self._data["facts"][key] = {
            "value": value,
            "updated_at": datetime.utcnow().isoformat() + "Z",
        }
        self._save()

    def get_fact(self, key: str) -> Optional[str]:
        entry = self._data["facts"].get(key)
        return entry["value"] if entry else None

    def add_employee_note(self, employee: str, note: str) -> None:
        emp = employee.strip().lower()
        self._data["employee_notes"].setdefault(emp, [])
        self._data["employee_notes"][emp].append({
            "note": note,
            "at": datetime.utcnow().isoformat() + "Z",
        })
        self._save()

    def get_employee_notes(self, employee: str) -> List[str]:
        emp = employee.strip().lower()
        notes = self._data["employee_notes"].get(emp, [])
        return [n["note"] for n in notes[-5:]]  # last 5

    def log_decision(self, agent: str, action: str, outcome: str) -> None:
        self._data["decisions"].append({
            "agent": agent,
            "action": action,
            "outcome": outcome[:200],
            "at": datetime.utcnow().isoformat() + "Z",
        })
        # keep last 50
        self._data["decisions"] = self._data["decisions"][-50:]
        self._save()

    def recent_decisions(self, n: int = 5) -> List[Dict]:
        return self._data["decisions"][-n:]

    def set_preference(self, key: str, value: str) -> None:
        self._data["preferences"][key] = value
        self._save()

    def get_preference(self, key: str, default: str = "") -> str:
        return self._data["preferences"].get(key, default)

    def search(self, query: str) -> str:
        """Simple keyword search over facts and notes."""
        q = query.lower()
        hits = []
        for k, v in self._data["facts"].items():
            if q in k.lower() or q in str(v.get("value", "")).lower():
                hits.append(f"Fact [{k}]: {v['value']}")
        for emp, notes in self._data["employee_notes"].items():
            if q in emp:
                for n in notes[-3:]:
                    hits.append(f"Note on {emp}: {n['note']}")
        if not hits:
            return "No matching long-term memory found."
        return "**Long-term memory hits:**\n\n" + "\n".join(f"- {h}" for h in hits[:8])


_ltm = None


def get_long_term() -> LongTermMemory:
    global _ltm
    if _ltm is None:
        _ltm = LongTermMemory()
    return _ltm
