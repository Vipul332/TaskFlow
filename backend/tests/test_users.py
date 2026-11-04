def test_get_users_requires_authentication(client):
    response = client.get("/api/users/")

    assert response.status_code == 401
    assert response.json["success"] is False


def test_get_users_success(auth_client, monkeypatch):
    from app.routes import users

    sample_users = [
        {
            "id": "user-123",
            "name": "Test User",
            "email": "test@example.com",
            "avatar_url": None,
        },
        {
            "id": "user-456",
            "name": "Another User",
            "email": "another@example.com",
            "avatar_url": None,
        },
    ]

    monkeypatch.setattr(
        users,
        "get_team_members",
        lambda: sample_users,
    )

    response = auth_client.get("/api/users/")

    assert response.status_code == 200
    assert response.json["success"] is True
    assert len(response.json["users"]) == 2
    assert response.json["users"][0]["email"] == "test@example.com"


def test_get_users_server_error(auth_client, monkeypatch):
    from app.routes import users

    def mock_get_team_members():
        raise Exception("Database connection failed")

    monkeypatch.setattr(
        users,
        "get_team_members",
        mock_get_team_members,
    )

    response = auth_client.get("/api/users/")

    assert response.status_code == 500
    assert response.json["success"] is False
    assert response.json["message"] == "Unable to fetch team members."