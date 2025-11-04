from repositories import Repository
from .mailings import MailingService
from .accounts import AccountsService
from .telegram import TelegramService
from .campaigns import CampaignsService
from .dialogs import DialogsService
from .ai import AIService
from .auth import AuthService


class Service:
	def __init__(self, repository: Repository):
		self.repository: Repository = repository

		self.ai: AIService = AIService()
		self.campaigns: CampaignsService = CampaignsService(self.repository)
		self.dialogs: DialogsService = DialogsService(self.repository)
		self.auth: AuthService = AuthService(self.repository)
		self.telegram: TelegramService = TelegramService(self.repository, self.ai)
		self.mailings: MailingService = MailingService(self.repository, self.telegram)
		self.accounts: AccountsService = AccountsService(self.repository, self.telegram)