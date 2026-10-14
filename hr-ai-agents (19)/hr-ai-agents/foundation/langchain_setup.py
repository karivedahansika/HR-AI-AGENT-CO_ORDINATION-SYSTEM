"""
LangChain configuration and agent foundation.

Uses LangChain message/prompt structures. LLM calls are optional:
if OPENAI_API_KEY (or similar) is not set, agents fall back to rule-based handlers.
"""

import os
from typing import List, Dict, Optional, Any

try:
    from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
    from langchain_core.prompts import ChatPromptTemplate
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    SystemMessage = HumanMessage = AIMessage = ChatPromptTemplate = None  # type: ignore

from prompts.templates import SYSTEM_PROMPTS, build_agent_prompt


def langchain_status() -> Dict[str, Any]:
    return {
        "langchain_installed": LANGCHAIN_AVAILABLE,
        "llm_configured": bool(os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")),
        "mode": "llm" if (LANGCHAIN_AVAILABLE and (os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY"))) else "rule_based",
    }


def build_langchain_messages(agent_key: str, user_message: str, context: str = "") -> list:
    """Convert our prompt template into LangChain message objects when available."""
    raw = build_agent_prompt(agent_key, user_message, context)
    if not LANGCHAIN_AVAILABLE:
        return raw
    out = []
    for m in raw:
        if m["role"] == "system":
            out.append(SystemMessage(content=m["content"]))
        elif m["role"] == "user":
            out.append(HumanMessage(content=m["content"]))
        else:
            out.append(AIMessage(content=m["content"]))
    return out


def get_chat_prompt_template(agent_key: str) -> Optional[Any]:
    """LangChain ChatPromptTemplate for the agent."""
    if not LANGCHAIN_AVAILABLE or ChatPromptTemplate is None:
        return None
    system = SYSTEM_PROMPTS.get(agent_key, SYSTEM_PROMPTS["orchestrator"])
    return ChatPromptTemplate.from_messages([
        ("system", system + "\n\nContext: {context}"),
        ("human", "{input}"),
    ])
