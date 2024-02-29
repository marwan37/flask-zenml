from pydantic import BaseModel, UUID4, Field
from typing import List, Dict


class StackComponentModel(BaseModel):
    id: UUID4
    name: str
    flavor: str
    type: str


class StackModel(BaseModel):
    id: UUID4
    name: str
    components: Dict[str, List[StackComponentModel]] = Field(default_factory=dict)
