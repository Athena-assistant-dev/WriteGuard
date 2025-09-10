import os
import configparser

REQUIRED_SECTIONS = {
    "server": ["host", "port"],
    "database": ["uri"],
    "auth": ["api_key"]
}

def validate_ini(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"[INI VALIDATOR] Config file not found: {file_path}")

    config = configparser.ConfigParser()
    config.read(file_path)

    errors = []

    for section, keys in REQUIRED_SECTIONS.items():
        if not config.has_section(section):
            errors.append(f"Missing section: [{section}]")
            continue
        for key in keys:
            if not config.has_option(section, key):
                errors.append(f"Missing option '{key}' in section [{section}]")

    if errors:
        raise ValueError("[INI VALIDATOR] Configuration validation errors:\n" + "\n".join(errors))
    else:
        print("[INI VALIDATOR] INI configuration is valid.")

if __name__ == "__main__":
    print("[INI VALIDATOR] Running test...")
    test_path = "test_config.ini"
    with open(test_path, "w") as f:
        f.write("""
[server]
host = localhost
port = 8000

[database]
uri = sqlite:///test.db

[auth]
api_key = samplekey
        """)

    try:
        validate_ini(test_path)
        print("[INI VALIDATOR] Test passed.")
    except Exception as e:
        print(f"[INI VALIDATOR] Test failed: {e}")
