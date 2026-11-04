def sample_task():
    return {
        "id": "task-123",
        "title": "Complete TaskFlow",
        "description": "Finish the internship assignment",
        "priority": "HIGH",
        "status": "TODO",
    }


def sample_user():
    return {
        "id": "user-123",
        "name": "Test User",
        "email": "test@example.com",
    }


def test_task_assigned_notification_success(monkeypatch):
    from app.services import notification_service

    sent_emails = []
    status_updates = []

    monkeypatch.setattr(
        notification_service,
        "create_notification",
        lambda data: {"id": "notification-123"},
    )

    monkeypatch.setattr(
        notification_service,
        "send_email",
        lambda **kwargs: sent_emails.append(kwargs),
    )

    monkeypatch.setattr(
        notification_service,
        "update_notification_status",
        lambda **kwargs: status_updates.append(kwargs),
    )

    result = notification_service.notify_task_assigned(
        sample_task(),
        sample_user(),
    )

    assert result is True
    assert len(sent_emails) == 1
    assert sent_emails[0]["to_email"] == "test@example.com"
    assert "New task assigned" in sent_emails[0]["subject"]
    assert status_updates[0]["status"] == "SENT"


def test_task_completed_notification_success(monkeypatch):
    from app.services import notification_service

    sent_emails = []
    status_updates = []

    monkeypatch.setattr(
        notification_service,
        "create_notification",
        lambda data: {"id": "notification-456"},
    )

    monkeypatch.setattr(
        notification_service,
        "send_email",
        lambda **kwargs: sent_emails.append(kwargs),
    )

    monkeypatch.setattr(
        notification_service,
        "update_notification_status",
        lambda **kwargs: status_updates.append(kwargs),
    )

    result = notification_service.notify_task_completed(
        sample_task(),
        sample_user(),
    )

    assert result is True
    assert len(sent_emails) == 1
    assert sent_emails[0]["to_email"] == "test@example.com"
    assert "Task completed" in sent_emails[0]["subject"]
    assert status_updates[0]["status"] == "SENT"


def test_assignment_notification_without_assignee():
    from app.services.notification_service import notify_task_assigned

    result = notify_task_assigned(sample_task(), None)

    assert result is False


def test_completion_notification_without_creator():
    from app.services.notification_service import notify_task_completed

    result = notify_task_completed(sample_task(), None)

    assert result is False


def test_notification_email_failure(monkeypatch):
    from app.services import notification_service

    status_updates = []

    monkeypatch.setattr(
        notification_service,
        "create_notification",
        lambda data: {"id": "notification-789"},
    )

    def mock_send_email(**kwargs):
        raise Exception("Gmail service unavailable")

    monkeypatch.setattr(
        notification_service,
        "send_email",
        mock_send_email,
    )

    monkeypatch.setattr(
        notification_service,
        "update_notification_status",
        lambda **kwargs: status_updates.append(kwargs),
    )

    result = notification_service.notify_task_assigned(
        sample_task(),
        sample_user(),
    )

    assert result is False
    assert status_updates[0]["status"] == "FAILED"
    assert "Gmail service unavailable" in status_updates[0]["error_message"]


def test_unsupported_notification_type():
    from app.services.notification_service import send_task_notification

    import pytest

    with pytest.raises(ValueError):
        send_task_notification(
            sample_task(),
            sample_user(),
            "INVALID_TYPE",
        )