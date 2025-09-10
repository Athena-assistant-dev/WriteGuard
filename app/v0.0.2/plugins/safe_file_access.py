import os
from plugins.file_map_tools import map_folder


SAFE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def safe_listdir(folder_path):
    """Attempt to list folder contents; map on failure."""
    try:
        return os.listdir(folder_path)
    except FileNotFoundError:
        map_folder(folder_path.replace("/srv", ""))
        raise

def safe_open(filepath, mode="r", *args, **kwargs):
    """Attempt to open file; map its folder on failure."""
    try:
        return open(filepath, mode, *args, **kwargs)
    except FileNotFoundError:
        map_folder(os.path.dirname(filepath).replace("/srv", ""))
        raise

def safe_isfile(filepath):
    """Check if file exists; map parent folder if not found."""
    if not os.path.isfile(filepath):
        map_folder(os.path.dirname(filepath).replace("/srv", ""))
        return False
    return True

def is_path_safe(path):
    abs_path = os.path.abspath(path)
    return abs_path.startswith(SAFE_ROOT)

def safe_read(path):
    with safe_open(path, "r") as f:
        return f.read()

def safe_write(path, content):
    with safe_open(path, "w") as f:
        f.write(content)
    print(f"[SAFE FILE ACCESS] Wrote to: {path}")

def safe_delete(path):
    if not is_path_safe(path):
        raise PermissionError(f"[SAFE FILE ACCESS] Unsafe delete path: {path}")
    if os.path.exists(path):
        os.remove(path)
        print(f"[SAFE FILE ACCESS] Deleted: {path}")
    else:
        print(f"[SAFE FILE ACCESS] File not found: {path}")

if __name__ == "__main__":
    print("[SAFE FILE ACCESS] Running test...")
    test_file = os.path.join(SAFE_ROOT, "test_data", "sample.txt")
    try:
        safe_write(test_file, "Safe I/O is working.")
        content = safe_read(test_file)
        print(f"[SAFE FILE ACCESS] Read content: {content}")
        safe_delete(test_file)
        print("[SAFE FILE ACCESS] Test passed.")
    except Exception as e:
        print(f"[SAFE FILE ACCESS] Test failed: {e}")
