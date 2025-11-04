from sqlalchemy.orm import Session
from sqlalchemy import Engine, func
from sqlalchemy.exc import IntegrityError

from schemas import CreateDialog
from .orm import Dialog as DialogORM


class DialogsORM:
    def __init__(self, orm: Engine):
        self.orm: Engine = orm
        
    def create(self, dialog: CreateDialog) -> int:
        with Session(self.orm) as session:
            dialog = DialogORM(**dialog.model_dump())
            session.add(dialog)
            session.commit()
            return dialog.id
        
    def get(self, **filters) -> list[DialogORM]:
        with Session(self.orm) as session:
            query = session.query(DialogORM)
            if filters:
                query = query.filter_by(**filters)
            return query.all()
            
    def get_by_id(self, dialog_id: int) -> DialogORM:
        with Session(self.orm) as session:
            return session.query(DialogORM).filter(DialogORM.id == dialog_id).first()
        
    def get_counts(self):
        with Session(self.orm) as session:
            return session.query(
                DialogORM.campaign_id,
                DialogORM.status,
                func.count(DialogORM.id)
            ).group_by(DialogORM.campaign_id, DialogORM.status).all()
        
    
