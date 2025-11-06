import asyncio
import logging
from repositories import Repository

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from repositories.orm import Account as AccountORM, Dialog as DialogORM
from schemas import CreateAccount, CreateMessage
from services.ai import AIService
from exceptions.accounts import *
from exceptions.telegram import *


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
            raise DuplicateAccountError
        
        session_name = f"Client_{account.username}"
        client = Client(session_name, session_string=account.session_string)
        handler = self.make_handler(account.id)
        client.add_handler(MessageHandler(handler, filters.text | filters.media))

        try:
            await client.start()
        except Exception:
            raise InvalidAccountData
        else:
            self.clients[account.id] = {"client": client, "handler": handler}
            logging.info(f"ADD CLIENT -- id: {account.id}, name: {session_name}")

    async def listen(self):
        while True:
            payload = await self.messages_queue.get()

            await self.process_message(
                client = payload["client"], 
                message = payload["message"]
            )

    async def process_message(self, client: Client, message: Message) -> str:
        dialog: DialogORM = self.repository.dialogs_orm.get(
            username = message.from_user.username,
            account_id = (await client.get_me()).id
        )[0]

        if dialog is None:
            logging.error(f"PROCESS MESSAGE -- {message.from_user.id} & {message.from_user.username}: '{message.text}'")
            return
    
        self.repository.messages_orm.create(CreateMessage(
            dialog_id = dialog.id,
            text = message.text,
            from_user = True
        ))

        # answer_text = await self.ai.get_answer(history)
        answer_text = "Анус мой нейросетевой облизал быстро, обезьяна лысая!"

        try:
            await message.reply(answer_text)

        except Exception as err:
            logging.error(f"PROCESS MESSAGE -- {message.from_user.id} & {message.from_user.username}: '{message.text}'")

        else:
            logging.info(f"PROCESS MESSAGE -- {message.from_user.id} & {message.from_user.username}: '{message.text}'")
            logging.info(f"SEND MESSAGE -- {dialog.account_id} --> {dialog.username}: '{answer_text}'")

            self.repository.messages_orm.create(CreateMessage(
                dialog_id = dialog.id,
                text = answer_text,
                from_user = False
            ))

    async def load_clients(self):
        accounts: list[AccountORM] = self.repository.accounts_orm.get(status="active")
        accounts = [CreateAccount.model_validate(account) for account in accounts]

        for account in accounts:
            await self.add_client(account)

    async def send_message(self, account_id: int, username: str, text: str):
        if account_id not in self.clients:
            raise ClientNotFoundError
        
        client = self.clients[account_id]['client']

        try:
            message = await client.send_message(chat_id=f"@{username}", text=text)
            logging.info(f"SEND MESSAGE -- {account_id} --> {username}: {text}")

        except Exception as err:
            logging.error(f"ERROR SEND MESSAGE -- {account_id} --> {username}: '{text}'")
            raise MessageSendError
        
        return message




    



