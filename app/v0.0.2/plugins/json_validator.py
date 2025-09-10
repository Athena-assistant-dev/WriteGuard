import os
import json

REQUIRED_KEYS = {
    "server": ["host", "port"],
    "auth": ["api_key"],
    "storage": ["path", "quota_gb"]
}

def validate_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"[JSON VALIDATOR] File not found: {file_path}")

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"[JSON VALIDATOR] Invalid JSON format: {e}")

    errors = []

    for top_key, sub_keys in REQUIRED_KEYS.items():
        if top_key not in data:
            errors.append(f"Missing top-level key: '{top_key}'")
            continue
        for sub_key in sub_keys:
            if sub_key not in data[top_key]:
                errors.append(f"Missing sub-key '{sub_key}' under '{top_key}'")

    if errors:
        raise ValueError("[JSON VALIDATOR] Validation errors:\n" + "\n".join(errors))
    else:
        print("[JSON VALIDATOR] JSON configuration is valid.")

if __name__ == "__main__":
    print("[JSON VALIDATOR] Running test...")
    test_file = "test_config.json"
    test_data = {
        "server": {"host": "localhost", "port": 8080},
        "auth": {"api_key": "secret"},
        "storage": {"path": "/data", "quota_gb": 100}
    }

    with open(test_file, "w") as f:
        json.dump(test_data, f, indent=2)

    try:
        validate_json(test_file)
        print("[JSON VALIDATOR] Test passed.")
    except Exception as e:
        print(f"[JSON VALIDATOR] Test failed: {e}")
