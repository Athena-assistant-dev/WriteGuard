import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))

GUARDED_EXTENSIONS = os.getenv("PROTECTED_EXTENSIONS", "").split(",")
PROTECTED_PATHS = os.getenv("PROTECTED_FILES_LIST", "").split(",")

def scan_for_risk(file_path, content):
    basename = os.path.basename(file_path)
    ext = os.path.splitext(basename)[1]

    if basename in PROTECTED_PATHS:
        raise PermissionError(f"[WRITE GUARD] Attempt to overwrite protected file: {basename}")

    if ext in GUARDED_EXTENSIONS:
        if ext == ".py" and (not content.strip() or not any(x in content for x in ["def ", "class ", "import "])):
            raise ValueError(f"[WRITE GUARD] Python file '{basename}' appears suspicious or empty.")
        if ext == ".json" and not content.strip().startswith("{"):
            raise ValueError(f"[WRITE GUARD] JSON file '{basename}' may be malformed.")
        if ext == ".ini" and "[" not in content:
            raise ValueError(f"[WRITE GUARD] INI file '{basename}' lacks section headers.")
        if ext == ".md" and len(content.strip().splitlines()) < 2:
            raise ValueError(f"[WRITE GUARD] Markdown file '{basename}' seems incomplete.")

    return True

if __name__ == "__main__":
    print("[WRITE GUARD] Running test...")
    try:
        test_file = "sample.py"
        test_content = "def hello():\n    print('Hi')\n"
        scan_for_risk(test_file, test_content)
        print("[WRITE GUARD] Test passed.")
    except Exception as e:
        print(f"[WRITE GUARD] Test failed: {e}")
