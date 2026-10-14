"""Base interface for enterprise API connectors."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseConnector(ABC):
    """Abstract connector – real systems would implement HTTP/SDK calls here."""

    name: str = "base"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.enabled = bool(self.config.get("enabled", True))

    @abstractmethod
    def connect(self) -> bool:
        """Establish connection / validate credentials."""

    @abstractmethod
    def execute(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Run an action against the external system."""

    def safe_execute(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Exception-safe wrapper for tool invocation."""
        try:
            if not self.enabled:
                return {"ok": False, "error": f"{self.name} connector disabled", "data": None}
            if not self.connect():
                return {"ok": False, "error": f"{self.name} connection failed", "data": None}
            result = self.execute(action, payload)
            return {"ok": True, "error": None, "data": result}
        except Exception as e:
            return {"ok": False, "error": str(e), "data": None}
