from repositories import Repository
from repositories.orm import Account as AccountORM
from schemas.account import CreateAccountResponse
from .telegram import TelegramService

from schemas import CreateAccount, Account


class AccountsService:
    def __init__(self, repository: Repository, telegram: TelegramService):
        self.repository: Repository = repository
        self.telegram: TelegramService = telegram

    async def create(self, account: CreateAccount) -> CreateAccountResponse:
        await self.telegram.add_client(account)
        account_id = self.repository.accounts_orm.create(account)
        return CreateAccountResponse(account_id=account_id)
    
    async def get(self) -> list[Account]:
        accounts: list[AccountORM] = self.repository.accounts_orm.get()
        return [Account.model_validate(account) for account in accounts]
    
    async def get_by_id(self, account_id: int) -> Account:
        account: AccountORM = self.repository.accounts_orm.get_by_id(account_id)
        return Account.model_validate(account)