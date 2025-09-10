import sys
import io
import traceback

def test_code_sandbox(code: str, filename="unspecified.py") -> dict:
    """
    Executes provided Python code in a sandboxed environment and returns stdout/stderr.
    Designed for previewing content before final write.
    """
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()

    # Backup original streams
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    sys.stdout = stdout_buffer
    sys.stderr = stderr_buffer

    result = {"success": True, "output": "", "error": ""}

    try:
        exec(code, {"__name__": "__main__", "__file__": filename})
    except Exception:
        result["success"] = False
        result["error"] = traceback.format_exc()
    finally:
        # Restore original streams
        sys.stdout = original_stdout
        sys.stderr = original_stderr

    result["output"] = stdout_buffer.getvalue().strip()
    return result
