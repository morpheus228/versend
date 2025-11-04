from sqlalchemy.orm import Session
from sqlalchemy import Engine, func
from sqlalchemy.exc import IntegrityError

from schemas import CreateUser
from .orm import InviteCode as InviteCodeORM
from .orm import User as UserORM


class AuthORM:
    def __init__(self, orm: Engine):
        self.orm: Engine = orm
        
    def get_invite_code(self, invite_code: str) -> InviteCodeORM|None:
        with Session(self.orm) as session:
            return session.query(InviteCodeORM).filter(InviteCodeORM.value == invite_code).first()
        
    def get_user(self, username: str) -> UserORM|None:
        with Session(self.orm) as session:
            return session.query(UserORM).filter_by(username=username).first()
        
    def create_user(self, user: CreateUser) -> int:
        with Session(self.orm) as session:
            user = UserORM(**user.model_dump())
            session.add(user)
            session.commit()
            return user.id
        
    def use_invite_code(self, invite_code: str):
        with Session(self.orm) as session:
            invite_code = session.query(InviteCodeORM).filter(InviteCodeORM.value == invite_code).first()
            invite_code.used = True
            session.commit()


