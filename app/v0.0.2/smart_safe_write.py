import os
import shutil
import hashlib
import json
import jsonpatch
import pytz
import tempfile
import subprocess
import difflib
import logging
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
from ruamel.yaml import YAML
from redbaron import RedBaron
from flask import jsonify

# Plugin integrations
from plugins.plugin_loader import validate_with_plugins, post_write_with_plugins, LOADED_PLUGINS
from plugins.pre_write_guard import scan_for_risk
from plugins.path_guard import is_allowed_path
from plugins.sandbox_exec import test_code_sandbox
from plugins.safe_file_access import safe_open
from plugins.time_utils import get_local_timestamp

# Add reader plugins
from plugins.docx_reader import after_write as docx_after_write
from plugins.xlsx_reader import after_write as xlsx_after_write
from plugins.pdf_reader import after_write as pdf_after_write
from plugins.pptx_reader import after_write as pptx_after_write
from plugins.image_reader import after_write as image_after_write

load_dotenv()

BASE_DIR = os.getenv("BASE_PATH", "./data")
VERSION_DIR = os.environ.get("VERSION_DIR_PATH", os.path.join(BASE_DIR, "json_mem", ".versions"))
BACKUP_DIR = os.environ.get("BACKUP_DIR_PATH", os.path.join(BASE_DIR, "json_mem", "write_backups"))
LOG_FOLDER = os.environ.get("LOG_FOLDER_PATH", os.path.join(BASE_DIR, "json_mem", "logs"))
LOG_PATH = os.path.join(LOG_FOLDER, "write_log.json")
IMMUTABLE_ENABLED = os.environ.get("ENABLE_IMMUTABLE_PROTECTION", "true").lower() == "true"
PROTECTED_FILES = [p.strip() for p in os.environ.get("PROTECTED_FILES_LIST", "").split(',') if p.strip()]

os.makedirs(LOG_FOLDER, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

# Setup logger
logger = logging.getLogger("smart_safe_write")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def is_binary(filepath):
    binary_extensions = [".docx", ".xlsx", ".pdf", ".pptx", ".jpg", ".jpeg", ".png", ".zip", ".gz", ".bin", ".exe", ".dll"]
    return any(filepath.lower().endswith(ext) for ext in binary_extensions)

def compute_hash(data):
    return hashlib.sha256(data).hexdigest()

def set_immutable(path, enable=True):
    if IMMUTABLE_ENABLED and shutil.which("chattr"):
        try:
            subprocess.run(["chattr", "+i" if enable else "-i", path], check=True)
        except Exception as e:
            print(f"[IMMUTABLE WARNING] chattr failed: {e}")

def is_protected(filepath):
    return any(filepath.endswith(p) for p in PROTECTED_FILES)
    
def get_local_timestamp_safe(*args, **kwargs):
    from plugins.time_utils import get_local_timestamp
    try:
        return get_local_timestamp(*args, **kwargs)
    except Exception as e:
        fallback_dt = datetime.now()
        logger.warning(f"[Timestamp Fallback] Using fallback due to: {e}")
        if kwargs.get("as_datetime"):
            return fallback_dt
        ts = fallback_dt.strftime("%Y-%m-%d_%H-%M-%S")
        ts_hash = hashlib.md5(ts.encode("utf-8")).hexdigest()[:6]
        return f"{ts}_{ts_hash}"


#this prunes logs only - variable in web gui
def prune_directory(directory, max_age_days, pattern="*.bak"):
    if not os.path.isdir(directory):
        return
    cutoff = get_local_timestamp_safe(as_datetime=True) - timedelta(days=max_age_days)
    for filename in Path(directory).glob(pattern):
        try:
            timestamp_str = filename.stem.split('.')[-1]
            file_time = datetime.strptime(timestamp_str, "%Y%m%d-%H%M%S")
            if file_time < cutoff:
                os.remove(filename)
                print(f"[PRUNING] Deleted old file: {filename}")
        except Exception:
            continue

def rotate_log():
    prune_directory(LOG_FOLDER, 7, pattern="*.bak")
    if os.path.exists(LOG_PATH) and os.path.getsize(LOG_PATH) > 100 * 1024**2:
        rotated_path = f"{LOG_PATH}.{get_local_timestamp_safe()}.bak"
        os.rename(LOG_PATH, rotated_path)

def get_versioned_path(filepath):
    os.makedirs(VERSION_DIR, exist_ok=True)
    timestamp = get_local_timestamp_safe()
    safe_name = filepath.replace("/", "__")
    return os.path.join(VERSION_DIR, f"{safe_name}.{timestamp}")

def generate_diff(old, new):
    return ''.join(difflib.unified_diff(
        old.splitlines(keepends=True),
        new.splitlines(keepends=True),
        fromfile='old', tofile='new'))

def safe_diff(old_content: str, new_content: str) -> str:
    return "".join(
        difflib.unified_diff(
            old_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            lineterm="",
        )
    )

def backup_file(filepath: str, backup_dir: str):
    """
    Create a timestamped backup of the given file.
    Backup filename format: [filename]_[pathhash]_[timestamp].bak
    """
    try:
        if not os.path.exists(filepath):
            logger.info(f"[Backup] Skipped - file does not exist: {filepath}")
            return

        # Generate safe relative path and hash
        rel_path = os.path.relpath(filepath, "/")
        path_hash = hashlib.md5(rel_path.encode("utf-8")).hexdigest()[:8]

        # Get timestamp from file_bridge_api (local timezone aware)
        timestamp = get_local_timestamp_safe()

        # Build backup filename
        base_name = os.path.basename(filepath)
        backup_name = f"{base_name}_{path_hash}_{timestamp}.bak"
        backup_path = os.path.join(backup_dir, backup_name)

        # Ensure directory exists
        os.makedirs(backup_dir, exist_ok=True)

        # Copy the file
        shutil.copy2(filepath, backup_path)
        logger.info(f"[Backup] Created: {backup_path}")   ##logger entry on every backup

    except Exception as e:
        logger.error(f"[Backup] Failed to create backup for {filepath}: {e}")


def prune_backups(filepath: str, backup_dir: str):
    """
    Prune backups for the given file based on age:
      - Keep 4 most recent backups for files ≤ 7 days old
      - Keep 2 backups for files 7–14 days old
      - Keep 1 backup for files older than 14 days
    """
    try:
        base_name = os.path.basename(filepath)
        rel_path = os.path.relpath(filepath, "/")
        path_hash = hashlib.md5(rel_path.encode("utf-8")).hexdigest()[:8]

        backups = []
        for f in os.listdir(backup_dir):
            if f.startswith(f"{base_name}_{path_hash}_") and f.endswith(".bak"):
                try:
                    ts_str = f.rsplit("_", 1)[-1].replace(".bak", "")
                    ts = datetime.strptime(ts_str, "%Y-%m-%d_%H-%M-%S")
                    backups.append((ts, f))
                except Exception:
                    continue

        # Sort by timestamp (newest first)
        backups.sort(key=lambda x: x[0], reverse=True)

        now = get_local_timestamp_safe(as_datetime=True)

        to_keep = []
        to_delete = []
        for ts, fname in backups:
            age_days = (now - ts).days
            if age_days <= 7:
                limit = 4
            elif age_days <= 14:
                limit = 2
            else:
                limit = 1

            current_group = [b for b in backups if (now - b[0]).days == age_days]
            if len(current_group) > limit:
                to_delete.extend(current_group[limit:])
                to_keep.extend(current_group[:limit])
            else:
                to_keep.extend(current_group)

        # Deduplicate keep list
        keep_set = {f for _, f in to_keep}
        for _, fname in backups:
            if fname not in keep_set:
                try:
                    os.remove(os.path.join(backup_dir, fname))
                    logger.info(f"[Prune] Removed old backup: {fname}")
                except Exception as e:
                    logger.error(f"[Prune] Failed to remove {fname}: {e}")

    except Exception as e:
        logger.error(f"[Prune] Error pruning backups for {filepath}: {e}")

## Main Function ##
def smart_safe_write(filepath, content_bytes=None, override=False, reason="unspecified", mode="default", patch=None, dry_run=False, preview=False):
    is_binary_file = is_binary(filepath)
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        old_content = b""
        pre_hash = None

        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                old_content = f.read()
            pre_hash = compute_hash(old_content)

            # --- NEW: backup before overwrite ---
            backup_file(filepath, BACKUP_DIR)
            prune_backups(filepath, BACKUP_DIR)  # keep history trimmed

        if not is_binary_file:
            decoded = content_bytes.decode("utf-8", errors="ignore")
            scan_for_risk(filepath, decoded)
            validate_with_plugins(filepath, decoded)
            if preview:
                test_code_sandbox(decoded, filepath)

        if dry_run:
            if preview and not is_binary_file:
                diff = generate_diff(old_content.decode('utf-8', errors='ignore'), content_bytes.decode('utf-8', errors='ignore'))
                return {"success": True, "written": False, "reason": "Dry run enabled", "diff": diff, "status": "dry_run"}
            return {"success": True, "written": False, "reason": "Dry run enabled", "status": "dry_run"}

        if mode == "patch" and not is_binary_file:
            if filepath.endswith(".json"):
                old_json = json.loads(old_content or b"{}")
                patched = jsonpatch.apply_patch(old_json, patch or [])
                content_bytes = json.dumps(patched, indent=2).encode("utf-8")
            elif filepath.endswith(('.yml', '.yaml')):
                yaml = YAML()
                data = yaml.load(old_content.decode("utf-8"))
                for op in patch or []:
                    exec(op, {}, {"data": data})
                import io
                buf = io.StringIO()
                yaml.dump(data, buf)
                content_bytes = buf.getvalue().encode("utf-8")
            else:
                return {"success": False, "error": "Unsupported patch file type"}

        elif mode == "ast" and not is_binary_file:
            red = RedBaron(old_content.decode("utf-8"))
            for change in patch or []:
                exec(change, {}, {"red": red})
            content_bytes = red.dumps().encode("utf-8")

        if old_content == content_bytes:
            return {"success": True, "written": False, "skipped": True, "reason": "Identical content"}

        if is_protected(filepath):
            set_immutable(filepath, enable=False)
        with tempfile.NamedTemporaryFile(delete=False, dir=os.path.dirname(filepath)) as tmp:
            tmp.write(content_bytes)
            tmp.flush()
            os.fsync(tmp.fileno())
            os.replace(tmp.name, filepath)
        if is_protected(filepath):
            set_immutable(filepath, enable=True)

        with open(filepath, 'rb') as f:
            read_back = f.read()
        post_hash = compute_hash(read_back)
        verified = post_hash == compute_hash(content_bytes)

        # CORRECTED BLOCK
        if not is_binary_file:
            decoded_content = content_bytes.decode('utf-8', errors='ignore')
            post_write_with_plugins(filepath, decoded_content)

        ext = os.path.splitext(filepath)[-1].lower()
        decoded_content = None if is_binary_file else content_bytes.decode("utf-8")
        if ext == ".docx":
            docx_after_write(filepath, decoded_content)
        elif ext == ".xlsx":
            xlsx_after_write(filepath, decoded_content)
        elif ext == ".pdf":
            pdf_after_write(filepath, decoded_content)
        elif ext == ".pptx":
            pptx_after_write(filepath, decoded_content)
        elif ext in [".jpg", ".jpeg", ".png"]:
            image_after_write(filepath, decoded_content)
            
        log_entry = {
            "timestamp": get_local_timestamp_safe(),
            "filename": filepath,
            "written": True,
            "verified": verified,
            "override": override,
            "mode": mode,
            "reason": reason,
            "pre_write_hash": pre_hash,
            "post_write_hash": post_hash
        }

        if mode != "light" and not is_binary_file:
            diff_path = get_versioned_path(filepath) + ".diff"
            with open(diff_path, 'w', encoding='utf-8') as df:
                df.write(generate_diff(old_content.decode('utf-8', errors='ignore'), content_bytes.decode('utf-8', errors='ignore')))

        rotate_log()
        with open(LOG_PATH, "a") as log_file:
            log_file.write(json.dumps(log_entry) + "\n")

        return {"success": True, "written": True, "verified": verified, "mode": mode}

    except Exception as e:
        return {"success": False, "error": str(e)}

def auto_map_on_failure(route_function):
    """
    Decorator to automatically catch errors in routes and provide safe responses
    without crashing the server.
    """
    from flask import jsonify, request

    def wrapper(*args, **kwargs):
        try:
            return route_function(*args, **kwargs)
        except FileNotFoundError as e:
            return jsonify({
                "error": "File not found",
                "details": str(e)
            }), 404
        except PermissionError as e:
            return jsonify({
                "error": "Permission denied",
                "details": str(e)
            }), 403
        except json.JSONDecodeError as e:
            return jsonify({
                "error": "Invalid JSON",
                "details": str(e)
            }), 400
        except Exception as e:
            logger.exception("Unhandled exception occurred")
            return jsonify({
                "error": "Internal server error",
                "details": str(e)
            }), 500

    wrapper.__name__ = route_function.__name__
    return wrapper
