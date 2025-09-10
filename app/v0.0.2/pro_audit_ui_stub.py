# pro_audit_ui_stub.py — Pro-only UI stub for audit log browsing
from pro_features import require_pro
from flask import Flask, jsonify
import os

app = Flask(__name__)

AUDIT_LOG_PATH = os.getenv("AUDIT_LOG_PATH", "/srv/logs/writeguard_audit.log")

@app.route("/pro/audit", methods=["GET"])
def get_audit_logs():
    require_pro("Audit Log Viewer")

    if not os.path.exists(AUDIT_LOG_PATH):
        return jsonify({"error": "No audit log found."}), 404

    with open(AUDIT_LOG_PATH, "r") as log:
        entries = log.readlines()[-100:]  # tail last 100 lines
    return jsonify({"entries": entries})

if __name__ == "__main__":
    app.run(port=5150)