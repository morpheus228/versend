from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str



class RegisterRequest(BaseModel):
    username: str
    password: str
    invite_code: str


class TokenResponse(BaseModel):
    token: str
    username: str


class CreateUser(BaseModel):
    username: str
    password_hash: str
    invite_code: str