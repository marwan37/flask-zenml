from app.models.stack import StackComponentModel


def serialize_stack_component(component) -> StackComponentModel:
    """Serializes a single stack component to a StackComponentModel instance."""
    return StackComponentModel(
        id=str(component.id),
        name=component.name,
        flavor=component.flavor,
        type=component.type,
    )