# langchain_tool.py — WriteGuard LangChain Tool wrapper
from langchain.tools import tool
import requests

@tool
def writeguard_write(filepath: str, content: str, reason: str = "llm_tool") -> str:
    """
    Perform a safe file write using WriteGuard. Pro mode summaries if enabled.
    """
    res = requests.post("http://localhost:5050/write", json={
        "filepath": filepath,
        "content": content,
        "reason": reason,
        "dry_run": False,
        "preview": True
    })
    return res.text