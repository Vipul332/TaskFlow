
from flask import Blueprint, current_app, jsonify, request

from app.services.auth_service import (
    verify_google_token,
    create_or_update_user
)
from app.middleware.auth_middleware import (
    get_session_serializer,
    get_current_user
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/google", methods=["POST"])
def google_login():
    data = request.get_json(silent=True) or {}
    google_token = data.get("credential")

    try:
        google_user = verify_google_token(
            google_token,
            current_app.config["GOOGLE_CLIENT_ID"]
        )

        user = create_or_update_user(google_user)

        session_token = get_session_serializer().dumps({
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "avatar_url": user.get("avatar_url")
        })

        response = jsonify({
            "success": True,
            "message": "Google login successful.",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "avatar_url": user.get("avatar_url")
            }
        })

        response.set_cookie(
            current_app.config["SESSION_COOKIE_NAME"],
            session_token,
            max_age=current_app.config["SESSION_MAX_AGE"],
            httponly=True,
            secure=current_app.config["SESSION_COOKIE_SECURE"],
            samesite=current_app.config["SESSION_COOKIE_SAMESITE"],
            path="/"
        )

        return response, 200

    except ValueError as exc:
        return jsonify({
            "success": False,
            "message": str(exc)
        }), 401

    except Exception:
        current_app.logger.exception("Google login failed")
        return jsonify({
            "success": False,
            "message": "Unable to complete Google login."
        }), 500


@auth_bp.route("/me", methods=["GET"])
def get_me():
    user = get_current_user()

    if not user:
        return jsonify({
            "success": False,
            "message": "Authentication required."
        }), 401

    return jsonify({
        "success": True,
        "user": user
    }), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({
        "success": True,
        "message": "Logged out successfully."
    })

    response.delete_cookie(
        current_app.config["SESSION_COOKIE_NAME"],
        path="/",
        httponly=True,
        secure=current_app.config["SESSION_COOKIE_SECURE"],
        samesite=current_app.config["SESSION_COOKIE_SAMESITE"]
    )

    return response, 200
