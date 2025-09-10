
import os
import base64
import mimetypes
from plugins.safe_file_access import safe_open, safe_isfile
from plugins.docx_reader import read_docx
from flask import jsonify

def read_file_generic(filepath):
    if not safe_isfile(filepath):
        return {"error": "File not found", "success": False}

    mime_type, _ = mimetypes.guess_type(filepath)
    ext = os.path.splitext(filepath)[-1].lower()

    try:
        if mime_type and mime_type.startswith("text"):
            with safe_open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                return {"content": f.read(), "success": True, "mime": mime_type}

        elif ext == ".docx":
            from plugins.docx_reader import read_docx  # Lazy import to avoid circular dependencies
            return {
                "content": read_docx(filepath),
                "success": True,
                "encoding": "text",
                "mime": mime_type or "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            }

        else:
            with safe_open(filepath, "rb") as f:
                content = base64.b64encode(f.read()).decode("utf-8")
            return {
                "content_b64": content,
                "success": True,
                "mime": mime_type or "application/octet-stream"
            }

    except Exception as e:
        return {"error": str(e), "success": False}
