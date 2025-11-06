from exceptions.accounts import *
from fastapi.responses import JSONResponse
from schemas.account import CreateAccountResponse
from services import Service
from schemas import CreateAccount

from fastapi import Response, HTTPException


class AccountsHandler:
    def __init__(self, service: Service):
        self.service: Service = service

    async def create(self, account: CreateAccount) -> CreateAccountResponse:
        try:
            return await self.service.accounts.create(account)
        
        except DuplicateAccountError as error:
            raise HTTPException(status_code=409, detail="Аккаунт с такими данными уже создан.")

        except InvalidAccountData as error:
            raise HTTPException(status_code=400, detail="Неудалось зарегистрировать аккаунт. Невалидные данные.")
    
    async def get(self) -> Response:
        accounts = await self.service.accounts.get()
        accounts_schema = [account.model_dump() for account in accounts]
        return JSONResponse(accounts_schema)
    
    async def get_by_id(self, account_id) -> Response:
        try:
            account = await self.service.accounts.get_by_id(account_id)
            account_schema = account.model_dump()
            return JSONResponse({"account": account_schema})

        except AccountNotFoundError as error:
            raise HTTPException(status_code=404, detail=str(error))



            



