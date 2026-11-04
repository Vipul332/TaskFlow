from flask import Blueprint, jsonify, current_app

from app.middleware.auth_middleware import require_auth
from app.services.user_service import get_team_members

users_bp = Blueprint("users", __name__)


@users_bp.route("/", methods=["GET"])
@require_auth
def get_users():
    """
    Get all registered TaskFlow users.
    """

    try:
        users = get_team_members()

        return jsonify({
            "success": True,
            "message": "Team members fetched successfully.",
            "users": users
        }), 200

    except Exception:
        current_app.logger.exception("Failed to fetch team members")

        return jsonify({
            "success": False,
            "message": "Unable to fetch team members."
        }), 500