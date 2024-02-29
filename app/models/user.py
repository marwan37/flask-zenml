from typing import Optional
from pydantic import UUID4, BaseModel


class UserModel(BaseModel):
    id: Optional[UUID4]
    name: Optional[str]
