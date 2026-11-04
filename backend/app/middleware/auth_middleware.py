
from functools import wraps

from flask import current_app, jsonify, request
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired


def get_session_serializer():
    return URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"],
        salt="taskflow-auth-session"
    )


def get_current_user():
    cookie_name = current_app.config["SESSION_COOKIE_NAME"]
    session_token = request.cookies.get(cookie_name)

    if not session_token:
        return None

    try:
        user_data = get_session_serializer().loads(
            session_token,
            max_age=current_app.config["SESSION_MAX_AGE"]
        )
        return user_data
    except (BadSignature, SignatureExpired):
        return None


def require_auth(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        user = get_current_user()

        if not user:
            return jsonify({
                "success": False,
                "message": "Authentication required."
            }), 401

        request.current_user = user
        return view_function(*args, **kwargs)

    return decorated_function
