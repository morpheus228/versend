import asyncio
from repositories import Repository
from repositories.orm import Dialog as DialogORM, Account as AccountORM, Campaign as CampaignORM
from services.telegram import TelegramService
from exceptions.telegram import MessageSendError
from schemas import CreateMessage


class MailingService:
    def __init__(self, repository: Repository, telegram: TelegramService):
        self.repository: Repository = repository
        self.telegram: TelegramService = telegram

    async def start(self):
        while True:
            dialog: DialogORM = self.repository.dialogs_orm.get_first(status="wait")

            if dialog is None:
                await asyncio.sleep(2)
                continue
            
            sender: AccountORM = await self.find_sender()
            await self.start_dialog(dialog, sender)

    async def find_sender(self) -> AccountORM:
        while True:
            account: AccountORM = self.repository.accounts_orm.get_free()
            if account is None: await asyncio.sleep(2)
            else: return account

    async def start_dialog(self, dialog: DialogORM, account: AccountORM):
        campaign: CampaignORM = self.repository.campaigns_orm.get_by_id(dialog.campaign_id)

        try:
            message = await self.telegram.send_message(
                account_id = account.id,
                username = dialog.username, 
                text = campaign.text
            )

        except MessageSendError:
            print("Ошибка отправки сообщения")

        else:

            # уменьшаем остаток сообщений на -1
            self.repository.accounts_orm.update(
                filters = {"id": account.id},
                values = {"messages_rest": account.messages_rest - 1}
            )

            # записываем сообщение в бд
            self.repository.messages_orm.create(CreateMessage(
                dialog_id = dialog.id,
                text = campaign.text,
                from_user = False
            ))

            # меняем статус диалога на open
            self.repository.dialogs_orm.update(
                filters = {"id": dialog.id},
                values = {
                    "status": "open",
                    "account_id": account.id
                },
            )

            



