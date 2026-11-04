
from app.repositories.task_repository import (
    create_task,
    get_task_by_id,
    update_task_status,
)
from app.repositories.user_repository import get_user_by_id
from app.services.notification_service import (
    notify_task_assigned,
    notify_task_completed,
)

ALLOWED_PRIORITIES = ["LOW", "MEDIUM", "HIGH", "URGENT"]
ALLOWED_STATUSES = ["TODO", "IN_PROGRESS", "COMPLETED"]


def create_task_service(data, creator_id):
    """
    Validate task details, verify assignee, create task,
    and notify the assigned team member.
    """

    # Validate title
    title = data.get("title", "")

    if not isinstance(title, str) or not title.strip():
        raise ValueError("Task title is required.")

    title = title.strip()

    if len(title) > 200:
        raise ValueError("Task title cannot exceed 200 characters.")

    # Validate description
    description = data.get("description", "")

    if description is not None and not isinstance(description, str):
        raise ValueError("Description must be a string.")

    if description and len(description) > 5000:
        raise ValueError("Description cannot exceed 5000 characters.")

    # Validate priority
    priority = data.get("priority", "MEDIUM")

    if not isinstance(priority, str):
        raise ValueError("Invalid task priority.")

    priority = priority.upper()

    if priority not in ALLOWED_PRIORITIES:
        raise ValueError("Invalid task priority.")

    # Validate assignee
    assignee_id = data.get("assignee_id")

    if assignee_id == "":
        assignee_id = None

    assignee = None

    if assignee_id is not None:
        if not isinstance(assignee_id, str):
            raise ValueError("Invalid assignee.")

        assignee = get_user_by_id(assignee_id)

        if not assignee:
            raise ValueError("Selected team member does not exist.")

    # Prepare task data
    task_data = {
        "title": title,
        "description": description.strip() if description else None,
        "creator_id": creator_id,
        "assignee_id": assignee_id,
        "priority": priority,
    }

    # Create task in database
    created_task = create_task(task_data)

    # Notify assignee after successful task creation
    if assignee:
        try:
            notify_task_assigned(created_task, assignee)
        except Exception:
            import logging
            logging.exception("Task created, but assignment notification failed.")

    return created_task


def update_task_status_service(task_id, new_status, current_user_id):
    """
    Validate permissions, update task status,
    and notify the creator when the task is completed.
    """

    if not isinstance(new_status, str):
        raise ValueError("Invalid task status.")

    new_status = new_status.upper()

    if new_status not in ALLOWED_STATUSES:
        raise ValueError("Invalid task status.")

    task = get_task_by_id(task_id)

    if not task:
        raise ValueError("Task not found.")

    # Only creator or assigned user can update the task.
    if (
        task["creator_id"] != current_user_id
        and task["assignee_id"] != current_user_id
    ):
        raise PermissionError("You are not allowed to update this task.")

    # Avoid unnecessary database updates and duplicate emails.
    if task["status"] == new_status:
        return task

    # Update task in database
    updated_task = update_task_status(task_id, new_status)

    # Notify creator only when task transitions to COMPLETED.
    if new_status == "COMPLETED":
        try:
            creator = get_user_by_id(task["creator_id"])

            if creator:
                notify_task_completed(updated_task, creator)

        except Exception:
            import logging
            logging.exception(
                "Task completed, but completion notification failed."
            )

    return updated_task
