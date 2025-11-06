from sqlalchemy import create_engine, BigInteger, String, Column, DateTime, ForeignKey, Boolean, Integer, Text, Float, Enum, JSON, func, text
from sqlalchemy.orm import declarative_base
from datetime import datetime

from config import Config


def get_orm():
    config = Config.mysql
    uri = f"mysql+pymysql://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}"
    return create_engine(uri)

Base = declarative_base()


class Account(Base):
    __tablename__ = 'Accounts'

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    phone_number = Column(String(20), nullable=False, unique=True)
    session_string = Column(String(512), nullable=False, unique=True)
    api_id = Column(BigInteger, nullable=False, unique=True)
    api_hash = Column(String(100), nullable=False, unique=True)
    username = Column(String(255), nullable=True, unique=True) 
    messages_rest = Column(BigInteger, nullable=False, default=20)
    status = Column(String(50), nullable=False, default="active")


class Campaign(Base):
    __tablename__ = 'Campaigns'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    text = Column(Text, nullable=False)
    promt = Column(Text, nullable=False)
    

class Dialog(Base):
    __tablename__ = 'Dialogs'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    account_id = Column(BigInteger, ForeignKey("Accounts.id", ondelete="CASCADE"), nullable=True)
    campaign_id = Column(BigInteger, ForeignKey("Campaigns.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(10), nullable=False) # open / closed / wait
    

class Message(Base):
    __tablename__ = 'Messages'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    dialog_id = Column(BigInteger, ForeignKey("Dialogs.id", ondelete="CASCADE"), nullable=False)
    text = Column(Text, nullable=False)
    from_user = Column(Boolean, nullable=False)

class InviteCode(Base):
    __tablename__ = 'InviteCodes'
    value = Column(String(32), nullable=False, primary_key=True)
    used = Column(Boolean, nullable=False, default=False) # open / closed
    notation = Column(String(50))

class User(Base):
    __tablename__ = 'Users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(32), nullable=False)
    password_hash = Column(String(100), nullable=False)
    invite_code = Column(String(32), ForeignKey("InviteCodes.value", ondelete="CASCADE"), nullable=False)










