from sqlalchemy.orm import Session
from sqlalchemy import Engine, func
from sqlalchemy.exc import IntegrityError

from exceptions.accounts import DuplicateAccountError

from .orm import Campaign as CampaignORM
from .orm import Dialog as DialogORM


class CampaignsORM:
    def __init__(self, orm: Engine):
        self.orm: Engine = orm
        
    def create(self, name: str, text: str, promt: str) -> int:
        with Session(self.orm) as session:
            campaign = CampaignORM(text=text, promt=promt, name=name)
            session.add(campaign)
            session.commit()
            return campaign.id
    
    def get(self, **filters) -> list[CampaignORM]:
        with Session(self.orm) as session:
            query = session.query(CampaignORM)
            if filters:
                query = query.filter_by(**filters)
            return query.all()
        
    def get_by_id(self, campaign_id: int) -> CampaignORM:
        with Session(self.orm) as session:
            return session.query(CampaignORM).filter(CampaignORM.id == campaign_id).first()




