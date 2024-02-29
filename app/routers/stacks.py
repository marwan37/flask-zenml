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