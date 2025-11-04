from datetime import datetime, timedelta

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from jose import jwt, JWTError

from repositories import Repository
from config import Config
from exceptions.auth import *
from repositories.orm import InviteCode as InviteCodeORM
from repositories.orm import User as UserORM

from schemas import RegisterRequest, LoginRequest, CreateUser

SECRET_KEY = "TJB9Vy1Eo8usYqMCPMmDUrNfBiHMoE6wDVW0TkbNCvsfyIriK66tTETv0ecqW4wu"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440


class AuthService:
    def __init__(self, repository: Repository):
        self.repository: Repository = repository

        self.hasher = PasswordHasher(
            time_cost=3,       # количество проходов
            memory_cost=65536, # использование памяти в KiB (64 MiB)
            parallelism=2      # количество потоков
        )

    def hash_password(self, password: str) -> str:
        return self.hasher.hash(password)
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        try:
            return self.hasher.verify(password_hash, password)
        except VerifyMismatchError:
            return False
        
    def create_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def get_user_id(self, token: str) -> int:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")

            if user_id is None:
                raise InvalidTokenError
            
        except JWTError:
            raise InvalidTokenError
        
        return user_id

    
    async def register(self, request: RegisterRequest) -> int:
        invite_code: InviteCodeORM = self.repository.auth_orm.get_invite_code(request.invite_code)

        if invite_code is None:
            raise InviteCodeNotFoundError
        
        if invite_code.used:
            raise ExpiredInviteCodeError

        user: UserORM = self.repository.auth_orm.get_user(request.username)

        if user is not None:
            raise UserAlreadyExistsError
        
        password_hash = self.hash_password(request.password)
        
        user_id = self.repository.auth_orm.create_user(
            CreateUser(
                username = request.username, 
                password_hash = password_hash,
                invite_code = request.invite_code
            )
        )

        self.repository.auth_orm.use_invite_code(request.invite_code)

        return user_id

    async def login(self, request: LoginRequest) -> str:
        user: UserORM = self.repository.auth_orm.get_user(request.username)

        if user is None:
            raise UserNotFoundError
        
        if not self.verify_password(request.password, user.password_hash):
            raise UserNotFoundError

        access_token = self.create_token({"sub": str(user.id)})

        return access_token        





    



