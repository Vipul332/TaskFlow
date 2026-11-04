from flask import Blueprint, jsonify, request, current_app

from app.middleware.auth_middleware import require_auth
from app.repositories.task_repository import get_tasks_for_user
from app.services.task_service import (
    create_task_service,
    update_task_status_service
)

tasks_bp = Blueprint("tasks", __name__)


# GET ALL TASKS
@tasks_bp.route("/", methods=["GET"])
@require_auth
def get_tasks():
    try:
        user = request.current_user
        tasks = get_tasks_for_user(user["id"])

        return jsonify({
            "success": True,
            "message": "Tasks fetched successfully.",
            "tasks": tasks
        }), 200

    except Exception:
        current_app.logger.exception("Failed to fetch tasks")

        return jsonify({
            "success": False,
            "message": "Unable to fetch tasks."
        }), 500


# CREATE A NEW TASK
@tasks_bp.route("/", methods=["POST"])
@require_auth
def create_task():
    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "success": False,
                "message": "A valid JSON request body is required."
            }), 400

        user = request.current_user

        task = create_task_service(
            data=data,
            creator_id=user["id"]
        )

        return jsonify({
            "success": True,
            "message": "Task created successfully.",
            "task": task
        }), 201

    except ValueError as exc:
        return jsonify({
            "success": False,
            "message": str(exc)
        }), 400

    except Exception:
        current_app.logger.exception("Failed to create task")

        return jsonify({
            "success": False,
            "message": "Unable to create task."
        }), 500


# UPDATE TASK STATUS
@tasks_bp.route("/<task_id>/status", methods=["PATCH"])
@require_auth
def update_task_status_route(task_id):
    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "success": False,
                "message": "A valid JSON request body is required."
            }), 400

        new_status = data.get("status")
        user = request.current_user

        task = update_task_status_service(
            task_id=task_id,
            new_status=new_status,
            current_user_id=user["id"]
        )

        return jsonify({
            "success": True,
            "message": "Task status updated successfully.",
            "task": task
        }), 200

    except ValueError as exc:
        return jsonify({
            "success": False,
            "message": str(exc)
        }), 400

    except PermissionError as exc:
        return jsonify({
            "success": False,
            "message": str(exc)
        }), 403

    except Exception:
        current_app.logger.exception("Failed to update task status")

        return jsonify({
            "success": False,
            "message": "Unable to update task status."
        }), 500