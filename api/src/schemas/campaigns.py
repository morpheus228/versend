from pydantic import BaseModel

from .dialogs import DialogList


class CreateCampaign(BaseModel):
    usernames: list[str]
    name: str
    text: str
    promt: str 

class CampaignList(BaseModel):
    id: int
    name: str
    text: str
    promt: str
    wait: int
    fail: int
    open: int
    stop: int

    model_config = {
        "from_attributes": True
    }

class Campaign(BaseModel):
    id: int
    name: str
    text: str
    promt: str
    dialogs: list[DialogList]
