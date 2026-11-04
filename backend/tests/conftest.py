import pytest
from itsdangerous import URLSafeTimedSerializer

from app import create_app


@pytest.fixture
def app():
    app = create_app()

    app.config.update(
        TESTING=True,
        SECRET_KEY="test-secret-key",
    )

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_client(client, app):
    user = {
        "id": "test-user-123",
        "name": "Test User",
        "email": "test@example.com",
        "avatar_url": None,
    }

    serializer = URLSafeTimedSerializer(
        app.config["SECRET_KEY"],
        salt="taskflow-auth-session",
    )

    session_token = serializer.dumps(user)

    client.set_cookie(
        app.config["SESSION_COOKIE_NAME"],
        session_token,
    )

    return client