# pro_features.py — optional pro-only logic toggle
import os

PRO_MODE = os.getenv("WRITEGUARD_PRO_MODE", "false").lower() == "true"


def is_pro_enabled() -> bool:
    return PRO_MODE


def require_pro(feature_name: str):
    if not is_pro_enabled():
        raise PermissionError(f"❌ '{feature_name}' is a Pro-only feature. Upgrade to unlock.")