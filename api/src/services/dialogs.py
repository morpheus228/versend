from repositories import Repository
from schemas import MessageList, Dialog
from repositories.orm import Dialog as DialogORM, Message as MessageORM


class DialogsService:
    def __init__(self, repository: Repository):
        self.repository: Repository = repository
    
    async def get_by_id(self, dialog_id) -> list[Dialog]:
        dialog: DialogORM = self.repository.dialogs_orm.get_by_id(dialog_id)
        messages: list[MessageORM] = self.repository.messages_orm.get(dialog_id=dialog.id)
        messages: list[MessageList] = [MessageList.model_validate(message) for message in messages]

        return Dialog(
            id = dialog.id,
            username = dialog.username,
            account_id = dialog.account_id,
            campaign_id = dialog.campaign_id,
            status = dialog.status,
            messages = messages
        )



        

