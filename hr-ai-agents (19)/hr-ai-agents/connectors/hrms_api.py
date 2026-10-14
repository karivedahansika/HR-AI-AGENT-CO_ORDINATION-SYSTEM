"""HRMS API connector stub (employee master, leave, etc.)."""

from typing import Any, Dict
from connectors.base import BaseConnector

# Mock employee store (would be real HRMS API)
_MOCK_EMPLOYEES = {
    "priya sharma": {"id": "EMP001", "dept": "Engineering", "status": "Active"},
    "amit patel": {"id": "EMP002", "dept": "Sales", "status": "Active"},
}


class HRMSConnector(BaseConnector):
    name = "hrms"

    def connect(self) -> bool:
        # In production: OAuth / API key check
        return True

    def execute(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if action == "get_employee":
            name = str(payload.get("name", "")).lower()
            emp = _MOCK_EMPLOYEES.get(name)
            if not emp:
                raise ValueError(f"Employee not found: {payload.get('name')}")
            return emp
        if action == "list_by_dept":
            dept = str(payload.get("dept", "")).lower()
            return {
                "employees": [
                    {"name": n.title(), **v}
                    for n, v in _MOCK_EMPLOYEES.items()
                    if v["dept"].lower() == dept
                ]
            }
        raise ValueError(f"Unknown HRMS action: {action}")
