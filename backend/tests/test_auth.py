def test_google_login_success(client, monkeypatch):
    from app.routes import auth

    google_user = {
        "google_id": "google-123",
        "email": "test@example.com",
        "name": "Test User",
        "avatar_url": "https://example.com/avatar.png",
    }

    saved_user = {
        "id": "user-123",
        "name": "Test User",
        "email": "test@example.com",
        "avatar_url": "https://example.com/avatar.png",
    }

    monkeypatch.setattr(
        auth,
        "verify_google_token",
        lambda token, client_id: google_user,
    )

    monkeypatch.setattr(
        auth,
        "create_or_update_user",
        lambda user_data: saved_user,
    )

    response = client.post(
        "/api/auth/google",
        json={"credential": "fake-google-token"},
    )

    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["user"]["id"] == "user-123"

    cookie = response.headers.get("Set-Cookie")
    assert "taskflow_session=" in cookie
    assert "HttpOnly" in cookie


def test_google_login_invalid_token(client, monkeypatch):
    from app.routes import auth

    def mock_verify_token(token, client_id):
        raise ValueError("Invalid or expired Google ID token.")

    monkeypatch.setattr(
        auth,
        "verify_google_token",
        mock_verify_token,
    )

    response = client.post(
        "/api/auth/google",
        json={"credential": "invalid-token"},
    )

    assert response.status_code == 401
    assert response.json["success"] is False


def test_google_login_missing_credential(client, monkeypatch):
    from app.routes import auth

    def mock_verify_token(token, client_id):
        raise ValueError("Google ID token is required.")

    monkeypatch.setattr(
        auth,
        "verify_google_token",
        mock_verify_token,
    )

    response = client.post(
        "/api/auth/google",
        json={},
    )

    assert response.status_code == 401
    assert response.json["success"] is False


def test_get_me_requires_authentication(client):
    response = client.get("/api/auth/me")

    assert response.status_code == 401
    assert response.json["success"] is False


def test_get_me_success(auth_client):
    response = auth_client.get("/api/auth/me")

    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["user"]["id"] == "test-user-123"
    assert response.json["user"]["email"] == "test@example.com"


def test_logout_success(auth_client):
    response = auth_client.post("/api/auth/logout")

    assert response.status_code == 200
    assert response.json["success"] is True

    # The session cookie should no longer authenticate the user.
    me_response = auth_client.get("/api/auth/me")

    assert me_response.status_code == 401