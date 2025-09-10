import argparse
from smart_safe_write import smart_safe_write
import os

if os.getenv("WRITEGUARD_PRO_MODE", "false").lower() == "true":
    from pro_diff_analyzer import summarize_diff


def main():
    parser = argparse.ArgumentParser(description="WriteGuard CLI")
    parser.add_argument("filepath", help="Path to the target file")
    parser.add_argument("--content", required=True, help="String content to write")
    parser.add_argument("--override", action="store_true", help="Override existing file")
    parser.add_argument("--reason", default="cli_write", help="Reason for write")
    parser.add_argument("--mode", default="default", help="Write mode")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the write without saving")
    parser.add_argument("--preview", action="store_true", help="Return file diff preview")
    parser.add_argument("--summary", action="store_true", help="Print Pro-only diff summary")

    args = parser.parse_args()

    result = smart_safe_write(
        filepath=args.filepath,
        content_bytes=args.content.encode("utf-8"),
        override=args.override,
        reason=args.reason,
        mode=args.mode,
        dry_run=args.dry_run,
        preview=args.preview
    )

    print(result)

    if args.summary and os.getenv("WRITEGUARD_PRO_MODE", "false").lower() == "true":
        old_text = result.get("original_content", "")
        new_text = args.content
        print("\n[Pro Diff Summary]")
        print(summarize_diff(old_text, new_text))

if __name__ == "__main__":
    main()