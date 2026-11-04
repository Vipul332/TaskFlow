
import logging

from app.repositories.notification_repository import (
    create_notification,
    update_notification_status,
)
from app.services.gmail_service import send_email

logger = logging.getLogger(__name__)


def send_task_notification(task, recipient, notification_type):
    """
    Create a notification record and send an email.
    Email failures are logged without interrupting task operations.
    """

    notification_id = None

    try:
        # Create a PENDING notification record.
        notification = create_notification({
            "task_id": task["id"],
            "recipient_id": recipient["id"],
            "type": notification_type,
            "status": "PENDING",
        })

        notification_id = notification["id"]

    except Exception:
        logger.exception("Could not create notification record")

    # Prepare email content.
    if notification_type == "TASK_ASSIGNED":
        subject = f"TaskFlow: New task assigned - {task['title']}"

        body = f"""
Hello {recipient['name']},

A new task has been assigned to you in TaskFlow.

Task: {task['title']}
Description: {task.get('description') or 'No description provided'}
Priority: {task['priority']}
Status: {task['status']}

Please log in to TaskFlow to view your task.

Regards,
TaskFlow Team
"""

    elif notification_type == "TASK_COMPLETED":
        subject = f"TaskFlow: Task completed - {task['title']}"

        body = f"""
Hello {recipient['name']},

Good news! A task you created has been marked as completed.

Task: {task['title']}
Description: {task.get('description') or 'No description provided'}
Status: COMPLETED

Please log in to TaskFlow to view the updated task.

Regards,
TaskFlow Team
"""

    else:
        raise ValueError(
            f"Unsupported notification type: {notification_type}"
        )

    # Attempt to send the email.
    try:
        send_email(
            to_email=recipient["email"],
            subject=subject,
            body=body,
        )

        logger.info(
            "Email notification sent: %s to %s",
            notification_type,
            recipient["email"],
        )

        if notification_id:
            try:
                update_notification_status(
                    notification_id=notification_id,
                    status="SENT",
                )
            except Exception:
                logger.exception(
                    "Email sent, but notification status update failed"
                )

        return True

    except Exception as exc:
        logger.exception(
            "Failed to send %s email to %s",
            notification_type,
            recipient["email"],
        )

        if notification_id:
            try:
                update_notification_status(
                    notification_id=notification_id,
                    status="FAILED",
                    error_message=str(exc)[:1000],
                )
            except Exception:
                logger.exception(
                    "Could not update failed notification status"
                )

        return False


def notify_task_assigned(task, assignee):
    """Notify a team member when a task is assigned."""

    if not assignee:
        return False

    return send_task_notification(
        task=task,
        recipient=assignee,
        notification_type="TASK_ASSIGNED",
    )


def notify_task_completed(task, creator):
    """Notify the task creator when their task is completed."""

    if not creator:
        return False

    return send_task_notification(
        task=task,
        recipient=creator,
        notification_type="TASK_COMPLETED",
    )
