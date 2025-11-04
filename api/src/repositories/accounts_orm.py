from sqlalchemy.orm import Session
from sqlalchemy import Engine
from sqlalchemy.exc import IntegrityError, NoResultFound

from exceptions.accounts import DuplicateAccountError, AccountNotFoundError
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

            except IntegrityError as error:
                session.rollback()
                raise DuplicateAccountError(error)
    
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
                raise AccountNotFoundError(error)



