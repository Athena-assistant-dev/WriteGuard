# pro_diff_analyzer.py — Pro-only enhanced diff analytics
import difflib
from pro_features import require_pro


def summarize_diff(old_text: str, new_text: str) -> dict:
    require_pro("Diff Analytics")

    diff = list(difflib.unified_diff(
        old_text.splitlines(), new_text.splitlines(), lineterm=""
    ))

    insertions = sum(1 for line in diff if line.startswith("+") and not line.startswith("+++"))
    deletions = sum(1 for line in diff if line.startswith("-") and not line.startswith("---"))

    return {
        "summary": {
            "insertions": insertions,
            "deletions": deletions,
            "total_changes": insertions + deletions
        },
        "raw_diff": diff
    }