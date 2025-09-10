# pro_dashboard_ui.py – Flask-based hosted dashboard (Pro-only)
from flask import Flask, render_template_string, request
import os
from pro_features import require_pro

app = Flask(__name__)

@app.route("/dashboard")
def dashboard():
    require_pro("Dashboard Access")

    return render_template_string("""
    <h1>🧩 WriteGuard Pro Dashboard</h1>
    <ul>
      <li><a href="/dashboard/audit">📜 View Audit Log</a></li>
      <li><a href="/dashboard/plugins">🔌 Plugin Settings</a></li>
    </ul>
    """)

@app.route("/dashboard/audit")
def audit_log():
    require_pro("Audit Log View")
    path = os.getenv("AUDIT_LOG_PATH", "/srv/logs/writeguard_audit.log")
    if not os.path.exists(path):
        return "No audit log found."
    with open(path) as f:
        lines = f.readlines()[-100:]
    return "<pre>" + "".join(lines) + "</pre>"

@app.route("/dashboard/plugins", methods=["GET", "POST"])
def plugin_config():
    require_pro("Plugin Configuration")
    # Stubbed demo logic
    if request.method == "POST":
        return "Plugins updated (stub)."
    return """
    <form method="post">
      <label><input type="checkbox" checked> .docx Plugin</label><br>
      <label><input type="checkbox" checked> .pdf Plugin</label><br>
      <input type="submit" value="Save">
    </form>
    """

if __name__ == "__main__":
    app.run(port=5151)