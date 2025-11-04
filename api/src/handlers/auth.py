from exceptions.auth import *
from fastapi.responses import JSONResponse
from schemas import LoginRequest, RegisterRequest
from services import Service

from fastapi import Body, Form, Response, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer


class AuthHandler:
    def __init__(self, service: Service):
        self.service: Service = service

    async def login(self, username: str = Form(...), password: str = Form(...)) -> Response:
        request: LoginRequest = LoginRequest(
            username = username, 
            password = password
        )

        try:
            access_token = await self.service.auth.login(request)

        except UserNotFoundError as error:
            raise HTTPException(status_code=401, detail=str(error))
        
        except InvalidPasswordError as error:
            raise HTTPException(status_code=401, detail=str(error))
        
        return JSONResponse({
            "access_token": access_token,
            "token_type": "bearer"
        })

    
    async def register(self, request: RegisterRequest) -> Response:
        try:
            user_id = await self.service.auth.register(request)

        except InviteCodeNotFoundError as error:
            raise HTTPException(status_code=404, detail=str(error))

        except ExpiredInviteCodeError as error:
            raise HTTPException(status_code=409, detail=str(error))
        
        except UserAlreadyExistsError as error:
            raise HTTPException(status_code=409, detail=str(error))
        
        return JSONResponse({"user_id": user_id})

    async def get_user_id(self, token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/login"))) -> int:
        try:
            return self.service.auth.get_user_id(token) 

        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

