from sqlalchemy.orm import Session
from sqlalchemy import Engine
from sqlalchemy.exc import IntegrityError, NoResultFound

from exceptions.accounts import *
from schemas import CreateAccount 

from .orm import Account as AccountORM


class AccountsORM:
    def __init__(self, orm: Engine):
        self.orm: Engine = orm
        
    def create(self, account: CreateAccount) -> int:
        with Session(self.orm) as session:

            try:
                account = AccountORM(**account.model_dump())
                session.add(account)
                session.commit()
                return account.id

            except IntegrityError:
                session.rollback()
                raise DuplicateAccountError
    
    def get(self, **filters) -> list[AccountORM]:
        with Session(self.orm) as session:
            query = session.query(AccountORM)
            if filters:
                query = query.filter_by(**filters)
            return query.all()
        
    def get_by_id(self, account_id) -> AccountORM:
        with Session(self.orm) as session:
            try:
                account = session.query(AccountORM).filter(AccountORM.id == account_id).one()
                return account
            except NoResultFound as error:
                raise AccountNotFoundError
            
    def get_free(self) -> AccountORM:
        with Session(self.orm) as session:
            return session.query(AccountORM).filter(AccountORM.messages_rest > 0).first()
        
    def update(self, filters: dict, values: dict):
        with Session(self.orm) as session:
            query = session.query(AccountORM)

            if filters:
                query = query.filter_by(**filters)

            query.update(values)
            session.commit()
            
            return query.all()





