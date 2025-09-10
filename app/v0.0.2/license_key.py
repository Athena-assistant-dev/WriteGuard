# license_key.py — simple license validation for Pro mode
import os

VALID_LICENSE_KEYS = {
    "WGPRO-1234-5678-90AB": "Terry Simmons",
    "WGPRO-A1B2-C3D4-E5F6": "Demo Org"
}

def is_license_valid(key: str) -> bool:
    return key in VALID_LICENSE_KEYS

def get_license_holder(key: str) -> str:
    return VALID_LICENSE_KEYS.get(key, "Unknown")


def require_valid_license():
    key = os.getenv("WRITEGUARD_LICENSE_KEY", "")
    if not is_license_valid(key):
        raise PermissionError("Invalid or missing WriteGuard license key.")