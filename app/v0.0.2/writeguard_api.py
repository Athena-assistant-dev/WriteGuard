# WriteGuard API v0.0.2
from flask import Flask, request, jsonify
from smart_safe_write import smart_safe_write
import os

app = Flask(__name__)

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

    if not filepath or content is None:
        return jsonify({"error": "Missing 'filepath' or 'content'"}), 400

    encoding = data.get("encoding")
    if encoding == "base64":
        import base64
        content_bytes = base64.b64decode(content)
    else:
        content_bytes = content.encode("utf-8")

    result = smart_safe_write(
        filepath=filepath,
        content_bytes=content_bytes,
        override=override,
        reason=reason,
        mode=mode,
        dry_run=dry_run,
        preview=preview
    )

    # Add Pro diff summary if applicable
    if os.getenv("WRITEGUARD_PRO_MODE", "false").lower() == "true" and result.get("original_content"):
        result["pro_summary"] = summarize_diff(result["original_content"], content)

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5050)), debug=True)