from services import Service
from exceptions import *
from schemas import CreateCampaign, Campaign

from fastapi import Response, HTTPException
from fastapi.responses import JSONResponse



class CampaignsHandler:
    def __init__(self, service: Service):
        self.service: Service = service

    async def create(self, campaign: CreateCampaign):
        campaign_id = await self.service.campaigns.create(campaign)
        return JSONResponse({"campaign_id": campaign_id})

    async def get(self) -> Response:
        campaigns = await self.service.campaigns.get()
        campaigns_schema = [campaign.model_dump() for campaign in campaigns]
        return JSONResponse(campaigns_schema)

    async def get_by_id(self, campaign_id: int) -> Response:
        campaign: Campaign = await self.service.campaigns.get_by_id(campaign_id)
        return JSONResponse(campaign.model_dump())        

    

        