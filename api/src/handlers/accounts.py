from exceptions.accounts import *
from fastapi.responses import JSONResponse
from services import Service
from schemas import CreateAccount

from fastapi import Response, HTTPException


class AccountsHandler:
    def __init__(self, service: Service):
        self.service: Service = service

    async def create(self, account: CreateAccount) -> Response:
        try:
            account_id = await self.service.accounts.create(account)
            return JSONResponse({"account_id": account_id})

        except DuplicateAccountError as error:
            raise HTTPException(status_code=409, detail=str(error))

        except InvalidAccountData as error:
            raise HTTPException(status_code=400, detail=str(error))
        
        # except Exception as error:
        #     raise HTTPException(status_code=500, detail=str(error))
        
    
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
        

    async def add_client(self, session_string: str):
        self.service
            



            



