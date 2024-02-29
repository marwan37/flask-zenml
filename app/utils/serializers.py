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
from app.models.stack import StackComponentModel


def serialize_stack_component(component) -> StackComponentModel:
    """
    Serializes a ZenML stack component object to a StackComponentModel instance.

    This function takes a ZenML stack component (such as an artifact store,
    orchestrator, etc.) and transforms it into a StackComponentModel object
    which includes its ID, name, flavor, and type.

    Parameters:
        component: The stack component to serialize. Expected to have 'id',
                   'name', 'flavor', and 'type' attributes.

    Returns:
        A StackComponentModel instance containing the serialized data of the
        input stack component.
    """
    return StackComponentModel(
        id=str(component.id),
        name=component.name,
        flavor=component.flavor,
        type=component.type,
    )