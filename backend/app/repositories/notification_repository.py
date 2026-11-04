
from app import extensions


def create_notification(notification_data):
    """
    Create a notification record in Supabase.
    Initial status is PENDING.
    """

    if extensions.supabase_client is None:
        raise RuntimeError("Supabase is not configured.")

    response = (
        extensions.supabase_client
        .table("notifications")
        .insert(notification_data)
        .execute()
    )

    if not response.data:
        raise RuntimeError("Unable to create notification record.")

    return response.data[0]


def update_notification_status(
    notification_id,
    status,
    error_message=None
):
    """
    Update notification status after attempting email delivery.
    """

    from datetime import datetime, timezone

    if extensions.supabase_client is None:
        raise RuntimeError("Supabase is not configured.")

    update_data = {
        "status": status,
        "error_message": error_message,
    }

    if status == "SENT":
        update_data["sent_at"] = datetime.now(
            timezone.utc
        ).isoformat()

    response = (
        extensions.supabase_client
        .table("notifications")
        .update(update_data)
        .eq("id", notification_id)
        .select("*")
        .execute()
    )

    if not response.data:
        raise RuntimeError("Unable to update notification record.")

    return response.data[0]
