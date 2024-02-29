from flask import Blueprint, jsonify
from app.utils.zen_client import call_zenml_api

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/", methods=["GET"])
def list_users():
    response = call_zenml_api("users", method="get")
    return jsonify(response), response.status_code


@bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    response = call_zenml_api(f"users/{user_id}", method="get")
    return jsonify(response), response.status_code
