from typing import Optional
from pydantic import BaseModel, Field


class ServerStatusModel(BaseModel):
    is_connected: bool
    host: Optional[str] = None
    port: Optional[int] = None
    store_type: str = Field(default=None, alias="storeType")
    store_url: str = Field(default=None, alias="storeUrl")
