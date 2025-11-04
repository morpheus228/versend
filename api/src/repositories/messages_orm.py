from sqlalchemy.orm import Session
from sqlalchemy import Engine, func
from sqlalchemy.exc import IntegrityError

from schemas import CreateMessage
from .orm import Message as MessageORM


class MessagesORM:
    def __init__(self, orm: Engine):
        self.orm: Engine = orm
        
    def create(self, message: CreateMessage) -> int:
        with Session(self.orm) as session:
            message = MessageORM(**message.model_dump())
            session.add(message)
            session.commit()
            return message.id
        
    def get(self, **filters) -> list[MessageORM]:
        with Session(self.orm) as session:
            query = session.query(MessageORM)
            if filters:
                query = query.filter_by(**filters)
            return query.all()
    
