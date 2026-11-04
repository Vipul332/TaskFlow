from app import extensions


def get_all_users():
    """
    Fetch all registered TaskFlow users.
    """

    if extensions.supabase_client is None:
        raise RuntimeError("Supabase is not configured.")

    response = (
        extensions.supabase_client
        .table("users")
        .select("id, name, email, avatar_url")
        .order("name")
        .execute()
    )

    return response.data or []

def get_user_by_id(user_id):
    """
    Fetch a registered user by their UUID.
    """

    if extensions.supabase_client is None:
        raise RuntimeError("Supabase is not configured.")

    response = (
        extensions.supabase_client
        .table("users")
        .select("id, name, email")
        .eq("id", user_id)
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]