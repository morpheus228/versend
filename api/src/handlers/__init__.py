from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .accounts import AccountsHandler
from .campaigns import CampaignsHandler
from .dialogs import DialogsHandler
from .auth import AuthHandler

from services import Service


class Handler:
    def __init__(self, service: Service):
        self.accounts = AccountsHandler(service)
        self.campaigns = CampaignsHandler(service)
        self.dialogs = DialogsHandler(service)
        self.auth = AuthHandler(service)
    
    def register(self, app: FastAPI):
        self.api_router = APIRouter(prefix="/api", dependencies=[Depends(self.auth.get_user_id)])
        self.auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

        self.accounts_router = APIRouter(prefix="/accounts", tags=["TelegramAccounts"])
        self.campaigns_router = APIRouter(prefix="/campaigns", tags=['Campaigns'])
        self.dialogs_router = APIRouter(prefix="/dialogs", tags=["Dialogs"])

        self.auth_router.add_api_route("/register", endpoint=self.auth.register, methods=["POST"])
        self.auth_router.add_api_route("/login", endpoint=self.auth.login, methods=["POST"])

        self.accounts_router.add_api_route("", endpoint=self.accounts.create, methods=["POST"]) # add telegram account
        self.accounts_router.add_api_route("", endpoint=self.accounts.get, methods=["GET"]) # get list of telegram accounts

        self.campaigns_router.add_api_route("", endpoint=self.campaigns.create, methods=["POST"]) # create mailing
        self.campaigns_router.add_api_route("", endpoint=self.campaigns.get, methods=["GET"]) # get list of mailings
        self.campaigns_router.add_api_route("/{campaign_id}", endpoint=self.campaigns.get_by_id, methods=["GET"])

        self.dialogs_router.add_api_route("/{dialog_id}", endpoint=self.dialogs.get_by_id, methods=["GET"])

        self.api_router.include_router(self.accounts_router)
        self.api_router.include_router(self.campaigns_router)
        self.api_router.include_router(self.dialogs_router)

        app.include_router(self.api_router)
        app.include_router(self.auth_router)

        origins = [
            "http://localhost:5173",   
            "http://127.0.0.1:5173",
        ]

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )