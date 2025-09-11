# WriteGuard API v0.0.2
from flask import Flask, request, jsonify
from smart_safe_write import smart_safe_write
import os
import logging
import difflib
import time

app = Flask(__name__)

BASE_DIR = os.environ.get("BASE_PATH", "")
if not BASE_DIR:
    raise RuntimeError("BASE_PATH is not set. Please configure it in your .env file or Web-GUI.")

AUDIT_LOG_PATH = os.path.join(BASE_DIR, "json_mem", "audit_log.txt")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

def log_audit(action, filename, status="success", client_ip=None):
    """Logs an audit event to the audit log file."""
    os.makedirs(os.path.dirname(AUDIT_LOG_PATH), exist_ok=True)
    entry = f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {action.upper():<6} | {filename} | {status} | {client_ip or 'N/A'}\n"
    with open(AUDIT_LOG_PATH, "a") as f:
        f.write(entry)

if os.getenv("WRITEGUARD_PRO_MODE", "false").lower() == "true":
    from pro_diff_analyzer import summarize_diff

@app.route("/write", methods=["POST"])
def write_file():
    data = request.json
    filepath = data.get("filepath")
    content = data.get("content")
    override = data.get("override", False)
    reason = data.get("reason", "unspecified")
    mode = data.get("mode", "default")
    dry_run = data.get("dry_run", False)
    preview = data.get("preview", False)
    action = "write"

    if not filepath or content is None:
        return jsonify({"error": "Missing 'filepath' or 'content'"}), 400

    full_path = os.path.join(BASE_DIR, filepath)
    
    logger.info(f"[5-STEP WRITE CHECK] Step 1: {action} request received for {full_path}")

    # Step 3: Diff or Binary Metadata
    is_binary = False
    encoding = data.get("encoding")
    if encoding == "base64":
        import base64
        content_bytes = base64.b64decode(content)
        is_binary = True
    else:
        content_bytes = content.encode("utf-8")

    if not is_binary and os.path.exists(full_path):
        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                old_content = f.read()
            diff = difflib.unified_diff(
                old_content.splitlines(),
                str(content).splitlines(),
                lineterm=""
            )
            changes = "\n".join(diff)
            logger.info(f"[5-STEP WRITE CHECK] Step 3: Diff generated ({len(changes.splitlines())} changes)")
        except Exception as e:
            logger.warning(f"[5-STEP WRITE CHECK] Step 3 skipped diff due to error: {e}")
    elif is_binary:
        logger.info(f"[5-STEP WRITE CHECK] Step 3: Binary file, skipping diff")

    # Step 4–5: Smart safe write with verification
    result = smart_safe_write(
        filepath=filepath,
        content_bytes=content_bytes,
        override=override,
        reason=reason,
        mode=mode,
        dry_run=dry_run,
        preview=preview
    )

    if not result.get("success"):
        logger.error(f"[5-STEP WRITE ERROR] smart_safe_write failed: {result.get('error')}")
        log_audit(action, full_path, "error")
        return jsonify(result)

    if not result.get("verified", False):
        logger.warning(f"[5-STEP WRITE WARNING] Post-write verification failed for {filepath}")
    else:
        logger.info(f"[5-STEP WRITE CHECK] Step 5: Verified write success for {filepath}")

    # Audit log
    log_audit(action, full_path, "success")

    # Add Pro diff summary if applicable
    if os.getenv("WRITEGUARD_PRO_MODE", "false").lower() == "true" and result.get("original_content"):
        result["pro_summary"] = summarize_diff(result["original_content"], content)

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5050)), debug=True)
