import asyncio
from repositories import Repository
from services.telegram import TelegramService


class MailingService:
    def __init__(self, repository: Repository, telegram: TelegramService):
        self.repository: Repository = repository
        self.telegram: TelegramService = telegram

    async def start(self):
        while True:
            message = await self.repository.messages_redis.get()

            if message is not None:
                await self.find_sender(message)

            await asyncio.sleep(2)
    
    async def find_sender(self, message: dict) -> int:
        while True:
            accounts = await self.repository.accounts_redis.get_list()

            for account_id in accounts.keys():
                if accounts[account_id] > 0:

                    message['account_id'] = account_id
                    print(message)

                    await self.send_message(message, account_id)
                    return account_id
            
    async def send_message(self, message: dict, account_id: int):
        await self.telegram.send_message(account_id, message['username'], message['text'])
        await self.repository.accounts_redis.update(account_id)


