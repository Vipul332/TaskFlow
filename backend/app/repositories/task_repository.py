from app import extensions


def get_tasks_for_user(user_id):
    """
    Fetch tasks created by or assigned to the logged-in user.
    """

    if extensions.supabase_client is None:
        raise RuntimeError("Supabase is not configured.")

    response = (
        extensions.supabase_client
        .table("tasks")
        .select(
            "*, creator:users!tasks_creator_id_fkey(id,name,email,avatar_url), "
            "assignee:users!tasks_assignee_id_fkey(id,name,email,avatar_url)"
        )
        .or_(f"creator_id.eq.{user_id},assignee_id.eq.{user_id}")
        .order("created_at", desc=True)
        .execute()
    )

    return response.data or []


def create_task(task_data):
    """
    Insert a new task into the database.
    """

    if extensions.supabase_client is None:
        raise RuntimeError("Supabase is not configured.")

    response = (
        extensions.supabase_client
        .table("tasks")
        .insert(task_data)
        .execute()
    )

    if not response.data:
        raise RuntimeError("Unable to create task.")

    return response.data[0]

def get_task_by_id(task_id):
    """
    Fetch a task using its UUID.
    """
    if extensions.supabase_client is None:
        raise RuntimeError("Supabase is not configured.")

    response = (
        extensions.supabase_client
        .table("tasks")
        .select("*")
        .eq("id", task_id)
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]


def update_task_status(task_id, status):
    """
    Update a task's status.
    """
    from datetime import datetime, timezone

    if extensions.supabase_client is None:
        raise RuntimeError("Supabase is not configured.")

    response = (
        extensions.supabase_client
        .table("tasks")
        .update({
            "status": status,
            "updated_at": datetime.now(timezone.utc).isoformat()
        })
        .eq("id", task_id)
        .select("*")
        .execute()
    )

    if not response.data:
        raise RuntimeError("Unable to update task status.")

    return response.data[0]