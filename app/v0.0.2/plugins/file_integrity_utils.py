import os
import time
import hashlib

def get_last_write_time(filepath):
    try:
        return os.path.getmtime(filepath)
    except FileNotFoundError:
        return 0

def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()

def is_suspicious_write(filepath, new_content_bytes):
    prior_size = os.path.getsize(filepath) if os.path.exists(filepath) else 0
    new_size = len(new_content_bytes)
    time_since_last_write = time.time() - get_last_write_time(filepath)

    # Rule 1: Minimum size threshold
    if prior_size > 0 and new_size < 0.2 * prior_size and time_since_last_write < 300:
        return True

    # Rule 2: Content checks for .py files
    if filepath.endswith(".py"):
        try:
            new_text = new_content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return True  # suspicious binary write to .py
        if not any(kw in new_text for kw in ["def ", "class ", "import "]):
            return True
        if len(new_text.strip()) < 50:
            return True

    # Rule 3: Content checks for .yaml files
    if filepath.endswith(".yaml"):
        try:
            new_text = new_content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return True
        if new_text.strip() == "" or len(new_text.splitlines()) < 10:
            return True

    # Rule 4: Content checks for .json files
    if filepath.endswith(".json"):
        try:
            import json
            new_data = json.loads(new_content_bytes.decode("utf-8"))
            if isinstance(new_data, dict) and len(new_data.keys()) < 5:
                return True
        except Exception:
            return True

    return False
