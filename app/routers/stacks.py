#  Copyright (c) ZenML GmbH 2024. All Rights Reserved.
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
import json
from flask import Blueprint, jsonify, request
from zenml.client import Client
from app.utils.global_config import fetch_active_user
from app.models.stack import StackModel
from app.utils.serializers import serialize_stack_component
from zenml.exceptions import IllegalOperationError, ZenKeyError

bp = Blueprint("stacks", __name__, url_prefix="/stacks")


@bp.route("", methods=["GET"])
@bp.route("/", methods=["GET"])
def fetch_stacks():
    """
    Fetches all ZenML stacks associated with the active user.

    Returns:
        JSON response with a list of stack models or 'error' on failure.
    """
    active_user_json = fetch_active_user()
    active_user = json.loads(active_user_json)
    user_id = active_user["id"]
    client = Client()
    stacks = client.list_stacks(hydrate=True, user_id=user_id)

    stacks_data = [
        StackModel(
            id=stack.id,
            name=stack.name,
            components={
                component_type: [serialize_stack_component(c) for c in components]
                for component_type, components in stack.components.items()
            },
        ).dict()
        for stack in stacks.items
    ]

    print(stacks_data)
    return jsonify(stacks_data)


@bp.route("/active_stack", methods=["GET"])
def active_stack():
    """
    Retrieves the currently active ZenML stack for the user.

    Returns:
        JSON response with the active stack model or 'error' on failure.
    """
    client = Client()
    try:
        current_stack = client.active_stack_model
        stack_components = {}

        for component_type, components in current_stack.components.items():
            stack_components[component_type] = [
                serialize_stack_component(c) for c in components
            ]

        stack_model = StackModel(
            id=current_stack.id, name=current_stack.name, components=stack_components
        )

        return jsonify(stack_model.dict())
    except Exception as e:
        error_model = {"error": str(e)}
        return jsonify(error_model), 500


@bp.route('/rename', methods=['POST'])
def rename_stack():
    """
    Renames a specified ZenML stack.

    Expects a JSON payload with 'stack_name_or_id' (the current name or ID of the stack) and
    'new_stack_name' (the new name for the stack).

    Returns:
        JSON response with 'message' indicating success or 'error' on failure.
    """
    data = request.json
    stack_name_or_id = data.get('stack_name_or_id')
    new_stack_name = data.get('new_stack_name')

    if not stack_name_or_id or not new_stack_name:
        return jsonify({'error': 'Missing stack_name_or_id or new_stack_name'}), 400

    client = Client()
    try:
        stack_ = client.update_stack(
            name_id_or_prefix=stack_name_or_id,
            name=new_stack_name,
        )
        return jsonify({'message': f'Stack `{stack_name_or_id}` successfully renamed to `{new_stack_name}`!'}), 200
    except (KeyError, IllegalOperationError) as err:
        return jsonify({'error': str(err)}), 400


@bp.route('/activate', methods=['POST'])
def set_active_stack():
    """
    Sets a specified ZenML stack as active.

    Expects a JSON payload with 'stack_name_or_id' specifying the stack to activate.

    Returns:
        JSON response with 'message' indicating success or 'error' on failure.
    """
    data = request.json
    stack_name_or_id = data.get('stack_name_or_id')

    if not stack_name_or_id:
        return jsonify({'error': 'Missing stack_name_or_id'}), 400

    client = Client()
    try:
        client.activate_stack(stack_name_id_or_prefix=stack_name_or_id)
        return jsonify({'message': f'Active stack set to: `{client.active_stack_model.name}`'}), 200
    except KeyError as err:
        return jsonify({'error': str(err)}), 400


@bp.route('/copy', methods=['POST'])
def copy_stack():
    """
    Copies a specified ZenML stack to a new stack with a given name.

    Expects a JSON payload with 'source_stack_name_or_id' (the name or ID of the stack to copy) and
    'target_stack' (the name for the new copied stack).

    Returns:
        JSON response with 'message' indicating success or 'error' on failure.
    """
    data = request.json
    source_stack_name_or_id = data.get('source_stack_name_or_id')
    target_stack_name = data.get('target_stack')

    if not source_stack_name_or_id or not target_stack_name:
        return jsonify({'error': 'Both source stack name/id and target stack name are required'}), 400

    client = Client()
    try:
        stack_to_copy = client.get_stack(name_id_or_prefix=source_stack_name_or_id)
        component_mapping = {c_type: [c.id for c in components][0] for c_type, components in
                             stack_to_copy.components.items() if components}

        copied_stack = client.create_stack(name=target_stack_name, components=component_mapping)
        return jsonify(
            {'message': f'Stack `{source_stack_name_or_id}` successfully copied to `{target_stack_name}`!'}), 200
    except ZenKeyError as err:
        return jsonify({'error': str(err)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500