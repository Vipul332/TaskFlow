
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-later")
    DEBUG = os.getenv("FLASK_DEBUG", "true").lower() == "true"

    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
           "CORS_ORIGINS",
            os.getenv("FRONTEND_URL", "http://localhost:3000")
        ).split(",")
        if origin.strip()
    ]

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

    SESSION_COOKIE_NAME = "taskflow_session"
    SESSION_COOKIE_SECURE = os.getenv(
        "SESSION_COOKIE_SECURE", "false"
    ).lower() == "true"
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
    SESSION_MAX_AGE = 60 * 60 * 24 * 7  # 7 days
