
import json
from pathlib import Path
from getpass import getpass

BASE_DIR = Path(__file__).resolve().parent

CLIENT_FILE = BASE_DIR / "credentials" / "gmail-oauth-client.json"
TOKEN_FILE = BASE_DIR / ".gmail-token.json"
ENV_FILE = BASE_DIR / ".env"

if not CLIENT_FILE.exists():
    raise FileNotFoundError("Gmail OAuth client JSON not found.")

if not TOKEN_FILE.exists():
    raise FileNotFoundError("Gmail token JSON not found.")

with CLIENT_FILE.open("r", encoding="utf-8") as file:
    client_data = json.load(file)

with TOKEN_FILE.open("r", encoding="utf-8") as file:
    token_data = json.load(file)

client_info = client_data.get("installed") or client_data.get("web")

if not client_info:
    raise ValueError("Invalid Google OAuth client JSON.")

client_id = client_info.get("client_id")
client_secret = client_info.get("client_secret")
refresh_token = token_data.get("refresh_token")

if not all([client_id, client_secret, refresh_token]):
    raise ValueError(
        "Missing client ID, client secret, or refresh token. "
        "Check the OAuth authorization."
    )

sender_email = input("Enter your authorized sender Gmail address: ").strip()

if "@" not in sender_email:
    raise ValueError("Enter a valid Gmail address.")

values = {
    "GMAIL_SENDER_EMAIL": sender_email,
    "GMAIL_CLIENT_ID": client_id,
    "GMAIL_CLIENT_SECRET": client_secret,
    "GMAIL_REFRESH_TOKEN": refresh_token,
}

existing_lines = ENV_FILE.read_text(encoding="utf-8").splitlines() if ENV_FILE.exists() else []

for key, value in values.items():
    existing_lines = [
        line for line in existing_lines
        if not line.startswith(f"{key}=")
    ]
    existing_lines.append(f"{key}={value}")

ENV_FILE.write_text(
    "\n".join(existing_lines) + "\n",
    encoding="utf-8"
)

print("\nGmail environment variables configured successfully!")
print("Credentials saved in backend/.env")
print("Credential values have not been displayed.")
