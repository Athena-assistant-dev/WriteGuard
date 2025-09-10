import os
import base64
from flask import Blueprint, request, jsonify

binary_api = Blueprint("binary_api", __name__)

BASE_DIR = "/srv"

def after_write(filepath, content):
    if any(filepath.endswith(ext) for ext in [".bin", ".dat", ".exe"]):
        print(f"[BINARY PLUGIN] Wrote: {filepath}, size: {len(content)} bytes")

@binary_api.route("/binary/read", methods=["POST"])
def read_binary_file():
    try:
        data = request.get_json()
        filepath = data.get("filepath")
        full_path = os.path.join(BASE_DIR, filepath)

        if not os.path.isfile(full_path):
            return jsonify({"error": "File not found", "success": False}), 404

        with open(full_path, "rb") as f:
            content = base64.b64encode(f.read()).decode('utf-8')

        return jsonify({
            "filename": os.path.basename(full_path),
            "content_base64": content,
            "success": True
        })
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500

@binary_api.route("/binary/write", methods=["POST"])
def write_binary_file():
    from smart_safe_write import smart_safe_write
    
    try:
        data = request.get_json()
        filepath = data.get("filepath")
        content_base64 = data.get("content_base64")

        if not filepath or not content_base64:
            return jsonify({"error": "Missing filepath or content", "success": False}), 400

        full_path = os.path.join(BASE_DIR, filepath)
        binary_data = base64.b64decode(content_base64)

        # Write via smart safe write
        result = smart_safe_write(full_path, binary_data, mode='binary')

        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500
