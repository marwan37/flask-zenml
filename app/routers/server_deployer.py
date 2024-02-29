import json
import logging
from flask import Blueprint, request, jsonify
from urllib.parse import urlparse
from zenml.zen_server.deploy.deployer import ServerDeployer
from zenml.zen_server.utils import get_active_server_details

from app.utils.zen_client import call_zenml_api
from app.utils.global_config import fetch_store_info, fetch_active_user
from app.models.server_status import ServerStatusModel
from zenml.cli import web_login
from app.utils.global_config import set_store_configuration

bp = Blueprint("server_deployer", __name__, url_prefix="/server_deployer")


@bp.route("/connect", methods=["POST"])
def connect():
    data = request.json
    url = data.get("url")
    verify_ssl = data.get("verify_ssl", True)

    if not url:
        return jsonify({"error": "Server URL is required."}), 400

    try:
        logging.info("Attempting web login...")
        access_token = web_login(url=url, verify_ssl=verify_ssl)
        logging.info(f"Web login successful, access_token: {access_token}")

        active_user_json = fetch_active_user()
        active_user = json.loads(active_user_json)
        user_id = active_user["id"]

        logging.info(f"Setting store configuration with user_id: {user_id}")
        set_store_configuration(remote_url=url, access_token=access_token, user_id=user_id)

        return jsonify({"message": "Connected successfully.", "access_token": access_token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/disconnect", methods=["POST"])
def disconnect():
    try:
        deployer = ServerDeployer()
        deployer.disconnect_from_server()
        return jsonify({"message": "Disconnected successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/status", methods=["GET"])
def status():
    store_info = fetch_store_info()
    store_type = store_info["store_type"]
    store_url = store_info["store_url"]

    try:
        url, port = get_active_server_details()
        parsed_url = urlparse(url)
        is_connected = False if store_type == "sql" else True

        server_status = ServerStatusModel(
            is_connected=is_connected,
            host=parsed_url.hostname,
            port=parsed_url.port if parsed_url.port else port,
            store_type=store_type if store_type == "sql" else None,
            store_url=store_url if store_type == "sql" else None,
        )
    except RuntimeError:
        server_status = ServerStatusModel(
            is_connected=False,
            host=None,
            port=None,
            store_type=store_type if store_type == "sql" else None,
            store_url=store_url if store_type == "sql" else None,
        )

    # Convert the Pydantic model to a dict before serializing to JSON
    return jsonify(server_status.dict(by_alias=True))


@bp.route("/info", methods=["GET"])
def get_server_info():
    """Get information about the ZenML server."""
    server_info = call_zenml_api("info")
    return jsonify(server_info)