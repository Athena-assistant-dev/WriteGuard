import os
import json
from datetime import datetime

MAP_DIR = "json_mem/maps"
os.makedirs(MAP_DIR, exist_ok=True)

explored_folders = set()  # In-memory tracker

def map_folder(folder_path):
    """Explore a folder and log its contents into memory and JSON map file."""
    try:
        if folder_path in explored_folders:
            return {"status": "already explored", "path": folder_path}

        full_path = os.path.join("/srv", folder_path)
        entries = os.listdir(full_path)
        mapped = []

        for entry in entries:
            full_entry_path = os.path.join(full_path, entry)
            mapped.append({
                "name": entry,
                "type": "dir" if os.path.isdir(full_entry_path) else "file",
                "size": os.path.getsize(full_entry_path),
                "modified": datetime.fromtimestamp(os.path.getmtime(full_entry_path)).isoformat()
            })

        # Save to JSON file
        map_file_path = os.path.join(MAP_DIR, f"{folder_path.replace('/', '_')}.map.json")
        with open(map_file_path, "w") as f:
            json.dump(mapped, f, indent=2)

        explored_folders.add(folder_path)
        return {"status": "mapped", "path": folder_path, "entries": mapped}

    except Exception as e:
        return {"status": "error", "path": folder_path, "error": str(e)}

def list_mapped_folders():
    """List all mapped folders (in-memory tracker)."""
    return list(explored_folders)

def read_map_file(folder_path):
    """Read contents of a map file."""
    try:
        map_file_path = os.path.join(MAP_DIR, f"{folder_path.replace('/', '_')}.map.json")
        with open(map_file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}