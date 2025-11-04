from sqlalchemy import Engine

from .accounts_orm import AccountsORM
from .campaigns_orm import CampaignsORM
from .dialogs_orm import DialogsORM
from .messages_orm import MessagesORM
from .auth_orm import AuthORM

from .orm import get_orm



class Repository:
	def __init__(self):
		self.orm: Engine = get_orm()

		self.accounts_orm: AccountsORM = AccountsORM(self.orm)
		self.campaigns_orm: CampaignsORM = CampaignsORM(self.orm)
		self.dialogs_orm: DialogsORM = DialogsORM(self.orm)
		self.messages_orm: MessagesORM = MessagesORM(self.orm)
		self.auth_orm: AuthORM = AuthORM(self.orm)