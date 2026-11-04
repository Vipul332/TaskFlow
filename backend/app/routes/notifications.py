
from flask import Blueprint, jsonify, request, current_app

from app.middleware.auth_middleware import require_auth
from app.repositories.notification_repository import (
    get_notifications_for_user,
)

notifications_bp = Blueprint("notifications", __name__)


@notifications_bp.route("/", methods=["GET"])
@require_auth
def get_notifications():
    """
    Fetch notifications for the currently logged-in user.
    """

    try:
        user = request.current_user

        notifications = get_notifications_for_user(user["id"])

        return jsonify({
            "success": True,
            "message": "Notifications fetched successfully.",
            "notifications": notifications,
        }), 200

    except Exception:
        current_app.logger.exception(
            "Failed to fetch notifications"
        )

        return jsonify({
            "success": False,
            "message": "Unable to fetch notifications.",
        }), 500
