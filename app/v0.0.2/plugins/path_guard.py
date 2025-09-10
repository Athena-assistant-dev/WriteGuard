import os
import json
from pathlib import Path
from datetime import datetime

# --- Configurable Policy Loader ---
def get_forbidden_subdirs():
    override_path = "/srv/json_mem/patch_override.json"
    gui_defined = []

    if os.path.exists(override_path):
        try:
            with open(override_path, "r") as f:
                data = json.load(f)
                gui_defined = data.get("FORBIDDEN_SUBDIRS", [])
        except Exception:
            pass

    if gui_defined:
        return gui_defined

    env_value = os.getenv("FORBIDDEN_SUBDIRS", "")
    return [item.strip() for item in env_value.split(",") if item.strip()]

# --- Centralized Access Control ---
def is_allowed_path(target_path: str) -> bool:
    base_dir = "/srv"
    abs_target = os.path.abspath(target_path)
    forbidden = get_forbidden_subdirs()

    try:
        rel_path = Path(abs_target).relative_to(base_dir)
        top_level = rel_path.parts[0] if len(rel_path.parts) > 0 else ""
    except Exception as e:
        with open("/srv/json_mem/logs/write_debug.log", "a") as log:
            log.write(f"[{datetime.now()}] Path resolution error: {e} → {abs_target}\n")
        return False

    if top_level in forbidden:
        with open("/srv/json_mem/logs/write_debug.log", "a") as log:
            log.write(f"[{datetime.now()}] Blocked write to {abs_target} (top-level: {top_level})\n")
        return False

    with open("/srv/json_mem/logs/write_debug.log", "a") as log:
        log.write(f"[{datetime.now()}] Allowed write to {abs_target} (top-level: {top_level})\n")

    return True
