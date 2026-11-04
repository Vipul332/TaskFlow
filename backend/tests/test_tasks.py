
def test_get_tasks_requires_authentication(client):
    response = client.get("/api/tasks/")

    assert response.status_code == 401
    assert response.json["success"] is False


def test_get_tasks_success(auth_client, monkeypatch):
    from app.routes import tasks

    sample_tasks = [
        {
            "id": "task-123",
            "title": "Complete assignment",
            "status": "TODO",
            "priority": "HIGH",
        }
    ]

    monkeypatch.setattr(
        tasks,
        "get_tasks_for_user",
        lambda user_id: sample_tasks,
    )

    response = auth_client.get("/api/tasks/")

    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["tasks"] == sample_tasks


def test_create_task_requires_authentication(client):
    response = client.post(
        "/api/tasks/",
        json={"title": "Test task"},
    )

    assert response.status_code == 401


def test_create_task_success(auth_client, monkeypatch):
    from app.routes import tasks

    sample_task = {
        "id": "task-123",
        "title": "Complete assignment",
        "description": "Finish the internship project",
        "creator_id": "test-user-123",
        "assignee_id": None,
        "status": "TODO",
        "priority": "HIGH",
    }

    def mock_create_task_service(data, creator_id):
        assert creator_id == "test-user-123"
        assert data["title"] == "Complete assignment"
        return sample_task

    monkeypatch.setattr(
        tasks,
        "create_task_service",
        mock_create_task_service,
    )

    response = auth_client.post(
        "/api/tasks/",
        json={
            "title": "Complete assignment",
            "description": "Finish the internship project",
            "priority": "HIGH",
            "assignee_id": None,
        },
    )

    assert response.status_code == 201
    assert response.json["success"] is True
    assert response.json["task"]["id"] == "task-123"


def test_create_task_rejects_invalid_data(auth_client):
    response = auth_client.post(
        "/api/tasks/",
        json={"title": ""},
    )

    assert response.status_code == 400
    assert response.json["success"] is False


def test_update_task_status_success(auth_client, monkeypatch):
    from app.routes import tasks

    updated_task = {
        "id": "task-123",
        "title": "Complete assignment",
        "status": "COMPLETED",
    }

    def mock_update_task_status_service(
        task_id,
        new_status,
        current_user_id,
    ):
        assert task_id == "task-123"
        assert new_status == "COMPLETED"
        assert current_user_id == "test-user-123"
        return updated_task

    monkeypatch.setattr(
        tasks,
        "update_task_status_service",
        mock_update_task_status_service,
    )

    response = auth_client.patch(
        "/api/tasks/task-123/status",
        json={"status": "COMPLETED"},
    )

    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["task"]["status"] == "COMPLETED"


def test_update_task_status_rejects_invalid_status(
    auth_client,
    monkeypatch,
):
    from app.routes import tasks

    def mock_update_task_status_service(
        task_id,
        new_status,
        current_user_id,
    ):
        raise ValueError("Invalid task status.")

    monkeypatch.setattr(
        tasks,
        "update_task_status_service",
        mock_update_task_status_service,
    )

    response = auth_client.patch(
        "/api/tasks/task-123/status",
        json={"status": "INVALID"},
    )

    assert response.status_code == 400
    assert response.json["success"] is False


def test_update_task_status_forbidden(auth_client, monkeypatch):
    from app.routes import tasks

    def mock_update_task_status_service(
        task_id,
        new_status,
        current_user_id,
    ):
        raise PermissionError(
            "You are not allowed to update this task."
        )

    monkeypatch.setattr(
        tasks,
        "update_task_status_service",
        mock_update_task_status_service,
    )

    response = auth_client.patch(
        "/api/tasks/task-123/status",
        json={"status": "COMPLETED"},
    )

    assert response.status_code == 403
    assert response.json["success"] is False


# TASK SERVICE TESTS


def test_task_service_create_success(monkeypatch):
    from app.services import task_service

    created_data = {}

    def mock_create_task(data):
        created_data.update(data)
        return {"id": "task-123", **data}

    monkeypatch.setattr(
        task_service,
        "create_task",
        mock_create_task,
    )

    result = task_service.create_task_service(
        {
            "title": "  Complete TaskFlow  ",
            "description": "  Finish assignment  ",
            "priority": "high",
        },
        "creator-123",
    )

    assert result["title"] == "Complete TaskFlow"
    assert result["description"] == "Finish assignment"
    assert result["priority"] == "HIGH"
    assert created_data["creator_id"] == "creator-123"


def test_task_service_create_with_assignee(monkeypatch):
    from app.services import task_service

    assignee = {
        "id": "assignee-123",
        "name": "Test Assignee",
        "email": "assignee@example.com",
    }

    monkeypatch.setattr(
        task_service,
        "get_user_by_id",
        lambda user_id: assignee,
    )

    monkeypatch.setattr(
        task_service,
        "create_task",
        lambda data: {"id": "task-123", **data},
    )

    notifications = []

    monkeypatch.setattr(
        task_service,
        "notify_task_assigned",
        lambda task, user: notifications.append((task, user)),
    )

    result = task_service.create_task_service(
        {
            "title": "Assigned task",
            "assignee_id": "assignee-123",
        },
        "creator-123",
    )

    assert result["assignee_id"] == "assignee-123"
    assert len(notifications) == 1


def test_task_service_rejects_invalid_title():
    import pytest
    from app.services.task_service import create_task_service

    with pytest.raises(ValueError, match="Task title is required"):
        create_task_service({"title": "   "}, "creator-123")


def test_task_service_rejects_long_title():
    import pytest
    from app.services.task_service import create_task_service

    with pytest.raises(ValueError, match="cannot exceed 200"):
        create_task_service(
            {"title": "A" * 201},
            "creator-123",
        )


def test_task_service_rejects_invalid_description():
    import pytest
    from app.services.task_service import create_task_service

    with pytest.raises(ValueError, match="Description must be a string"):
        create_task_service(
            {
                "title": "Valid task",
                "description": 123,
            },
            "creator-123",
        )


def test_task_service_rejects_invalid_priority():
    import pytest
    from app.services.task_service import create_task_service

    with pytest.raises(ValueError, match="Invalid task priority"):
        create_task_service(
            {
                "title": "Valid task",
                "priority": "SUPER",
            },
            "creator-123",
        )


def test_task_service_rejects_nonexistent_assignee(monkeypatch):
    import pytest
    from app.services import task_service

    monkeypatch.setattr(
        task_service,
        "get_user_by_id",
        lambda user_id: None,
    )

    with pytest.raises(
        ValueError,
        match="Selected team member does not exist",
    ):
        task_service.create_task_service(
            {
                "title": "Valid task",
                "assignee_id": "unknown-user",
            },
            "creator-123",
        )


def test_task_service_update_status_success(monkeypatch):
    from app.services import task_service

    existing_task = {
        "id": "task-123",
        "creator_id": "creator-123",
        "assignee_id": "assignee-123",
        "status": "TODO",
    }

    updated_task = {
        **existing_task,
        "status": "IN_PROGRESS",
    }

    monkeypatch.setattr(
        task_service,
        "get_task_by_id",
        lambda task_id: existing_task,
    )

    monkeypatch.setattr(
        task_service,
        "update_task_status",
        lambda task_id, status: updated_task,
    )

    result = task_service.update_task_status_service(
        "task-123",
        "in_progress",
        "assignee-123",
    )

    assert result["status"] == "IN_PROGRESS"


def test_task_service_rejects_unauthorized_user(monkeypatch):
    import pytest
    from app.services import task_service

    existing_task = {
        "id": "task-123",
        "creator_id": "creator-123",
        "assignee_id": "assignee-123",
        "status": "TODO",
    }

    monkeypatch.setattr(
        task_service,
        "get_task_by_id",
        lambda task_id: existing_task,
    )

    with pytest.raises(
        PermissionError,
        match="not allowed to update",
    ):
        task_service.update_task_status_service(
            "task-123",
            "COMPLETED",
            "unauthorized-user",
        )


def test_task_service_rejects_missing_task(monkeypatch):
    import pytest
    from app.services import task_service

    monkeypatch.setattr(
        task_service,
        "get_task_by_id",
        lambda task_id: None,
    )

    with pytest.raises(ValueError, match="Task not found"):
        task_service.update_task_status_service(
            "missing-task",
            "COMPLETED",
            "creator-123",
        )


def test_task_service_skips_duplicate_status_update(monkeypatch):
    from app.services import task_service

    existing_task = {
        "id": "task-123",
        "creator_id": "creator-123",
        "assignee_id": None,
        "status": "COMPLETED",
    }

    monkeypatch.setattr(
        task_service,
        "get_task_by_id",
        lambda task_id: existing_task,
    )

    def should_not_update(task_id, status):
        raise AssertionError("Unnecessary database update occurred")

    monkeypatch.setattr(
        task_service,
        "update_task_status",
        should_not_update,
    )

    result = task_service.update_task_status_service(
        "task-123",
        "COMPLETED",
        "creator-123",
    )

    assert result == existing_task


def test_task_service_sends_completion_notification(monkeypatch):
    from app.services import task_service

    existing_task = {
        "id": "task-123",
        "creator_id": "creator-123",
        "assignee_id": "assignee-123",
        "status": "IN_PROGRESS",
    }

    updated_task = {
        **existing_task,
        "status": "COMPLETED",
    }

    creator = {
        "id": "creator-123",
        "name": "Task Creator",
        "email": "creator@example.com",
    }

    monkeypatch.setattr(
        task_service,
        "get_task_by_id",
        lambda task_id: existing_task,
    )

    monkeypatch.setattr(
        task_service,
        "update_task_status",
        lambda task_id, status: updated_task,
    )

    monkeypatch.setattr(
        task_service,
        "get_user_by_id",
        lambda user_id: creator,
    )

    notifications = []

    monkeypatch.setattr(
        task_service,
        "notify_task_completed",
        lambda task, user: notifications.append((task, user)),
    )

    result = task_service.update_task_status_service(
        "task-123",
        "COMPLETED",
        "assignee-123",
    )

    assert result["status"] == "COMPLETED"
    assert len(notifications) == 1
    assert notifications[0][1]["id"] == "creator-123"
