
from google.auth.transport import requests
from google.oauth2 import id_token

from app import extensions


def verify_google_token(google_token, client_id):
    """
    Verify the Google ID token and return trusted user information.
    """

    if not google_token:
        raise ValueError("Google ID token is required.")

    if not client_id:
        raise RuntimeError("Google Client ID is not configured.")

    try:
        payload = id_token.verify_oauth2_token(
            google_token,
            requests.Request(),
            client_id
        )
    except ValueError as exc:
        raise ValueError(
            "Invalid or expired Google ID token."
        ) from exc

    if not payload.get("email_verified"):
        raise ValueError("Google email is not verified.")

    google_id = payload.get("sub")
    email = payload.get("email")

    if not google_id or not email:
        raise ValueError("Google account information is incomplete.")

    return {
        "google_id": google_id,
        "email": email.lower(),
        "name": payload.get("name") or email.split("@")[0],
        "avatar_url": payload.get("picture")
    }


def create_or_update_user(user_data):
    """
    Insert a new Google user or update an existing user.
    """

    if extensions.supabase_client is None:
        raise RuntimeError("Supabase is not configured.")

    response = (
        extensions.supabase_client
        .table("users")
        .upsert(user_data, on_conflict="google_id")
        .execute()
    )

    if not response.data:
        raise RuntimeError("Unable to save user in database.")

    return response.data[0]
