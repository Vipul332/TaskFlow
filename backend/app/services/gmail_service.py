
import os
import base64
from pathlib import Path
from email.mime.text import MIMEText

from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


# Load backend environment variables
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

GMAIL_SCOPE = "https://www.googleapis.com/auth/gmail.send"


def get_gmail_service():
    """
    Authenticate with Gmail API using credentials from backend/.env.
    """

    client_id = os.getenv("GMAIL_CLIENT_ID")
    client_secret = os.getenv("GMAIL_CLIENT_SECRET")
    refresh_token = os.getenv("GMAIL_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        raise RuntimeError(
            "Gmail credentials are missing from the backend .env file."
        )

    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=[GMAIL_SCOPE],
    )

    service = build(
        "gmail",
        "v1",
        credentials=credentials,
        cache_discovery=False,
    )

    return service


def send_email(to_email, subject, body):
    """
    Send a plain-text email through Gmail API.
    """

    sender_email = os.getenv("GMAIL_SENDER_EMAIL")

    if not sender_email:
        raise RuntimeError("GMAIL_SENDER_EMAIL is missing from .env.")

    if not to_email or "@" not in to_email:
        raise ValueError("A valid recipient email address is required.")

    if not subject or not body:
        raise ValueError("Email subject and body are required.")

    message = MIMEText(body)
    message["to"] = to_email
    message["from"] = sender_email
    message["subject"] = subject

    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode("utf-8")

    service = get_gmail_service()

    result = service.users().messages().send(
        userId="me",
        body={"raw": encoded_message},
    ).execute()

    return {
        "success": True,
        "message_id": result.get("id"),
    }
