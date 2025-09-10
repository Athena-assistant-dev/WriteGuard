import os

REQUIRED_ENV_VARS = [
    "API_KEY",
    "DB_URI",
    "STORAGE_PATH",
    "MODEL_DIR",
    "SERVER_PORT"
]

def validate_env():
    missing = []
    for var in REQUIRED_ENV_VARS:
        if not os.environ.get(var):
            missing.append(var)

    if missing:
        raise EnvironmentError(f"[ENV VALIDATOR] Missing required environment variables: {', '.join(missing)}")
    else:
        print("[ENV VALIDATOR] All required environment variables are set.")

if __name__ == "__main__":
    print("[ENV VALIDATOR] Running test...")

    # Setup test environment variables
    os.environ["API_KEY"] = "testkey"
    os.environ["DB_URI"] = "sqlite:///db.sqlite3"
    os.environ["STORAGE_PATH"] = "/data/storage"
    os.environ["MODEL_DIR"] = "/models"
    os.environ["SERVER_PORT"] = "8080"

    try:
        validate_env()
        print("[ENV VALIDATOR] Test passed.")
    except EnvironmentError as e:
        print(str(e))
