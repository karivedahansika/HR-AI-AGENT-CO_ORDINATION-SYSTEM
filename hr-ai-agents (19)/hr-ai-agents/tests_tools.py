"""Basic tests for tool invocation and connector exception handling."""

from tools.tool_router import use_tool
from connectors.hrms_api import HRMSConnector
from connectors.email_api import EmailConnector
from foundation.langchain_setup import langchain_status


def test_tools():
    assert use_tool("Screen resume for Data Analyst") is not None
    assert "Resume" in use_tool("Screen resume for Data Analyst")
    assert use_tool("Generate interview questions for HR") is not None
    assert use_tool("Leave balance for Priya Sharma") is not None
    assert use_tool("Check maternity policy") is not None
    assert use_tool("Generate onboarding plan for Engineer") is not None
    assert use_tool("hello world random") is None
    print("Tool selection tests: PASSED")


def test_connectors():
    hrms = HRMSConnector()
    r = hrms.safe_execute("get_employee", {"name": "Priya Sharma"})
    assert r["ok"] is True
    r2 = hrms.safe_execute("get_employee", {"name": "Unknown Person"})
    assert r2["ok"] is False
    email = EmailConnector()
    r3 = email.safe_execute("draft", {"to": "a@b.com", "body": "Hello"})
    assert r3["ok"] is True
    r4 = email.safe_execute("draft", {"to": "a@b.com", "body": ""})
    assert r4["ok"] is False
    print("Connector exception handling tests: PASSED")


def test_langchain_foundation():
    status = langchain_status()
    assert "langchain_installed" in status
    assert "mode" in status
    print("LangChain foundation status:", status)
    print("LangChain foundation tests: PASSED")


if __name__ == "__main__":
    test_tools()
    test_connectors()
    test_langchain_foundation()
    print("\nAll Milestone 1–2 tool/connector tests passed.")
