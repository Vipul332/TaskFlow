from app.repositories.user_repository import get_all_users


def get_team_members():
    """
    Business logic for retrieving registered team members.
    """

    return get_all_users()