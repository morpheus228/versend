from pydantic import BaseModel
from enum import Enum

from .messages import MessageList


class CreateDialog(BaseModel):
    username: str
    campaign_id: int
    status: str


class DialogList(BaseModel):
    id: int
    username: str
    account_id: int|None
    campaign_id: int
    status: str

    model_config = {
        "from_attributes": True
    }

class Dialog(BaseModel):
    id: int
    username: str
    account_id: int|None
    campaign_id: int
    status: str

    messages: list[MessageList]
