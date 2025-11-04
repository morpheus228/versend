import asyncio
from repositories import Repository

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from repositories.orm import Account as AccountORM
from schemas import CreateAccount
from services.ai import AIService
from exceptions.accounts import InvalidAccountData


class TelegramService:
    def __init__(self, repository: Repository, ai: AIService):
        self.repository: Repository = repository
        self.ai: AIService = ai

        self.messages_queue = asyncio.Queue()
        self.clients = {}

    def make_handler(self, account_id: int):
        async def handler(client: Client, message: Message):

            await self.messages_queue.put({
                "client": client,
                "message": message,
            })
        return handler
    
    async def add_client(self, account: CreateAccount):
        if account.id in self.clients:
            raise RuntimeError(f"Client with key {account.id} already exists")
        
        session_name = f"Client_{account.username}"
        client = Client(session_name, session_string=account.session_string)

        handler = self.make_handler(account.id)
        client.add_handler(MessageHandler(handler, filters.text | filters.media))

        try:
            await client.start()
        except Exception as err:
            raise InvalidAccountData(err)

        self.clients[account.id] = {"client": client, "handler": handler}

        print(f"Аккаунт {session_name} добавлен!")

    async def listen(self):
        while True:
            payload = await self.messages_queue.get()

            client: Client = payload["client"]
            message: Message = payload["message"]
            chat_id = message.chat.id

            # Получаем историю сообщений (например, последние 50)
            history = []
            async for msg in client.get_chat_history(chat_id, limit=50):
                history.append({
                    "text": msg.text,
                    "from_user": not msg.from_user.is_self
                })

            answer = await self.ai.get_answer(history)
            await message.reply_text(answer)


    async def load_clients(self):
        accounts: list[AccountORM] = self.repository.accounts_orm.get(status="active")
        accounts = [Account.model_validate(account) for account in accounts]

        for account in accounts:
            await self.add_client(account)

    async def send_message(self, account_id: int, recipient_id: int, text: str):
        client = self.clients[account_id]['client']
        message = await client.send_message(chat_id=recipient_id, text=text)
        return message




    



