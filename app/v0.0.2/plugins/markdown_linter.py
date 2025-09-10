import os
import re

REQUIRED_HEADERS = [
    "# Overview",
    "## Installation",
    "## Usage",
    "## Configuration",
    "## License"
]

def lint_markdown(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"[MARKDOWN LINTER] File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    errors = []

    for header in REQUIRED_HEADERS:
        if header not in content:
            errors.append(f"Missing required header: {header}")

    trailing_ws_lines = [i + 1 for i, line in enumerate(content.splitlines()) if line.rstrip() != line]
    if trailing_ws_lines:
        errors.append(f"Trailing whitespace on lines: {trailing_ws_lines}")

    if re.search(r"\n{3,}", content):
        errors.append("More than two consecutive blank lines")

    if errors:
        raise ValueError("[MARKDOWN LINTER] Lint errors:\n" + "\n".join(errors))
    else:
        print("[MARKDOWN LINTER] Markdown is clean.")

if __name__ == "__main__":
    print("[MARKDOWN LINTER] Running test...")
    test_md = "test_doc.md"
    with open(test_md, "w") as f:
        f.write("""
# Overview

## Installation

## Usage

## Configuration

## License

Text with trailing spaces.    
Another line.

        
        
Final line.
        """)

    try:
        lint_markdown(test_md)
        print("[MARKDOWN LINTER] Test passed.")
    except Exception as e:
        print(f"[MARKDOWN LINTER] Test failed: {e}")
