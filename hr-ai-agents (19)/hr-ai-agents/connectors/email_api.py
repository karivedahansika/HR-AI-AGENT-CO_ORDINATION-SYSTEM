"""Email API connector stub (Outlook/Gmail Graph would go here)."""

from typing import Any, Dict
from connectors.base import BaseConnector


class EmailConnector(BaseConnector):
    name = "email"

    def connect(self) -> bool:
        return True

    def execute(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if action == "draft":
            to = payload.get("to", "[Recipient]")
            subject = payload.get("subject", "HR Communication")
            body = payload.get("body", "")
            if not body:
                raise ValueError("Email body is required")
            return {"to": to, "subject": subject, "body": body, "status": "drafted"}
        if action == "send":
            # Simulated send
            return {"status": "queued", "id": "MSG-SIM-001"}
        raise ValueError(f"Unknown email action: {action}")
