from flask import Blueprint, jsonify
import os, time, json

file_map_bp = Blueprint("file_map_bp", __name__)

@file_map_bp.route("/file-structure-map/rebuild", methods=["POST"])
def rebuild_file_structure():
    from smart_safe_write import smart_safe_write
    base_path = "/srv"
    structure = {}

    for root, dirs, files in os.walk(base_path):
        for name in dirs + files:
            full_path = os.path.join(root, name)
            try:
                rel_path = os.path.relpath(full_path, base_path)
                stats = os.stat(full_path)
                structure[rel_path] = {
                    "type": "folder" if os.path.isdir(full_path) else "file",
                    "size": stats.st_size,
                    "modified": time.ctime(stats.st_mtime),
                }
            except Exception as e:
                structure[rel_path] = {"error": str(e)}

    result_path = os.path.join("/srv", "json_mem", "file_structure_map.json")
    result = smart_safe_write(result_path, json.dumps(structure, indent=2), reason="rebuild-file-structure-map")
    return jsonify({"message": "Structure rebuilt", "path": result})