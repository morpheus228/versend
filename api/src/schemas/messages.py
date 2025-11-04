from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class CreateMessage(BaseModel):
    dialog_id: int
    text: int
    from_user: bool


class MessageList(BaseModel):
    id: int
    dialog_id: int
    text: str
    from_user: bool
    
    model_config = {
        "from_attributes": True
    }
