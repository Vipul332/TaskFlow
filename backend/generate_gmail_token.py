
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

BASE_DIR = Path(__file__).resolve().parent

CLIENT_SECRET_FILE = (
    BASE_DIR / "credentials" / "gmail-oauth-client.json"
)

TOKEN_FILE = BASE_DIR / ".gmail-token.json"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]


def generate_token():
    if not CLIENT_SECRET_FILE.exists():
        raise FileNotFoundError(
            f"Credentials file not found: {CLIENT_SECRET_FILE}"
        )

    flow = InstalledAppFlow.from_client_secrets_file(
        str(CLIENT_SECRET_FILE),
        scopes=SCOPES
    )

    credentials = flow.run_local_server(
        port=0,
        access_type="offline",
        prompt="consent"
    )

    TOKEN_FILE.write_text(credentials.to_json())

    print("\nGmail authorization successful!")
    print(f"Token saved securely at: {TOKEN_FILE}")


if __name__ == "__main__":
    generate_token()
