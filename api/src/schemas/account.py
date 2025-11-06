from pydantic import BaseModel
from enum import Enum


class CreateAccount(BaseModel):
    id: int
    username: str|None
    phone_number: str
    api_id: int
    api_hash: str
    session_string: str

    model_config = {
        "from_attributes": True
    }


class CreateAccountResponse(BaseModel):
    account_id: int


class Account(BaseModel):
    id: int
    username: str|None
    phone_number: str
    api_id: int
    api_hash: str
    session_string: str

    model_config = {
        "from_attributes": True
    }


    
