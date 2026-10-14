"""
Short-term memory: holds the current conversation context (this session).
"""

from collections import deque
from typing import List, Dict, Any


class ShortTermMemory:
    """In-session conversation memory (last N turns)."""

    def __init__(self, max_turns: int = 20):
        self.max_turns = max_turns
        self._messages: deque = deque(maxlen=max_turns * 2)  # user + assistant pairs
        self._context: Dict[str, Any] = {}

    def add(self, role: str, content: str) -> None:
        self._messages.append({"role": role, "content": content})

    def get_history(self, last_n: int = 10) -> List[Dict[str, str]]:
        items = list(self._messages)
        return items[-last_n:] if last_n else items

    def get_context_summary(self) -> str:
        """Compact summary of recent conversation for agents."""
        history = self.get_history(6)
        if not history:
            return ""
        lines = []
        for m in history:
            prefix = "User" if m["role"] == "user" else "Assistant"
            snippet = m["content"][:120].replace("\n", " ")
            lines.append(f"{prefix}: {snippet}")
        return "\n".join(lines)

    def set_fact(self, key: str, value: Any) -> None:
        """Store a short-lived fact for this session (e.g. current employee name)."""
        self._context[key] = value

    def get_fact(self, key: str, default=None) -> Any:
        return self._context.get(key, default)

    def clear(self) -> None:
        self._messages.clear()
        self._context.clear()


# Global session instance (Streamlit can also keep its own)
_session_memory = ShortTermMemory()


def get_short_term() -> ShortTermMemory:
    return _session_memory
