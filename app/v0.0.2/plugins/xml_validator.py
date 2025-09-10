import os
import xml.etree.ElementTree as ET

REQUIRED_TAGS = [
    "config",
    "server",
    "database",
    "auth"
]

def validate_xml(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"[XML VALIDATOR] File not found: {file_path}")

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        raise ValueError(f"[XML VALIDATOR] Invalid XML format: {e}")

    errors = []

    for tag in REQUIRED_TAGS:
        if root.find(tag) is None:
            errors.append(f"Missing required tag: <{tag}>")

    if errors:
        raise ValueError("[XML VALIDATOR] Validation errors:\n" + "\n".join(errors))
    else:
        print("[XML VALIDATOR] XML configuration is valid.")

if __name__ == "__main__":
    print("[XML VALIDATOR] Running test...")
    test_file = "test_config.xml"
    with open(test_file, "w") as f:
        f.write("""
<config>
    <server>
        <host>localhost</host>
        <port>8000</port>
    </server>
    <database>
        <uri>sqlite:///db.sqlite3</uri>
    </database>
    <auth>
        <api_key>abc123</api_key>
    </auth>
</config>
        """)

    try:
        validate_xml(test_file)
        print("[XML VALIDATOR] Test passed.")
    except Exception as e:
        print(f"[XML VALIDATOR] Test failed: {e}")
