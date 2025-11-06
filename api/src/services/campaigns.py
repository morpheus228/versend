from exceptions.dialogs import DuplicateDialogError
from repositories import Repository
from schemas import CreateCampaign, Campaign, CreateDialog, CampaignList, DialogList, CreateCampaignResponse
from repositories.orm import Campaign as CampaignORM


class CampaignsService:
    def __init__(self, repository: Repository):
        self.repository: Repository = repository

    async def create(self, campaign: CreateCampaign) -> CreateCampaignResponse:
        campaign_id = self.repository.campaigns_orm.create(
            text = campaign.text, 
            promt = campaign.promt, 
            name = campaign.name
        )

        duplicate_usernames: list[str] = list()

        for username in campaign.usernames:
            try:
                self.repository.dialogs_orm.create(CreateDialog(
                    username  = username,
                    campaign_id = campaign_id,
                    status = "wait"
                ))
                
            except DuplicateDialogError:
                duplicate_usernames.append(username)

        return CreateCampaignResponse(
            campaign_id = campaign_id,
            duplicate_usernames = duplicate_usernames
        )

    async def get(self) -> list[CampaignList]:
        campaigns: list[CampaignORM] = self.repository.campaigns_orm.get()
        dialog_counts = self.repository.dialogs_orm.get_counts()

        result = {}

        for campaign in campaigns:
            result[campaign.id] = {
                "id": campaign.id,
                "name": campaign.name,
                "text": campaign.text,
                "promt": campaign.promt,
                "wait": 0, 
                "fail": 0, 
                "open": 0, 
                "stop": 0
            }

        for campaign_id, status, count in dialog_counts:

            result[campaign_id][status] = count

        return [CampaignList(**campaign) for campaign in result.values()]
    
    async def get_by_id(self, campaign_id) -> list[Campaign]:
        campaign = self.repository.campaigns_orm.get_by_id(campaign_id)
        dialogs = self.repository.dialogs_orm.get(campaign_id=campaign_id)
        dialogs = [DialogList.model_validate(dialog) for dialog in dialogs]

        return Campaign(
            id = campaign.id,
            name = campaign.name,
            text = campaign.text,
            promt = campaign.promt,
            dialogs = dialogs
        )



        

