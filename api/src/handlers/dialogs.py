from services import Service
from exceptions import *

from fastapi import Response, HTTPException
from fastapi.responses import JSONResponse


class DialogsHandler:
    def __init__(self, service: Service):
        self.service: Service = service

    async def get_by_id(self, dialog_id: int) -> Response:
        dialog = await self.service.dialogs.get_by_id(dialog_id)
        return JSONResponse(dialog.model_dump())        
