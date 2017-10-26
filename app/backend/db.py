import os
import sys
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    # Here we define columns for the table person
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)

class Account(Base):
    __tablename__ = 'account'
    # Here we define columns for the table Account.
    id = Column(Integer, primary_key=True)
    cur_amount = Column(Float, default=0)
    isTrade = Column(Boolean)    #check if the account is trade account
    # account_trade_amount and tradetime record the change on Account directly
    account_trade_amount = Column(Float, default=0)
    tradetime = Column(DateTime, default=datetime.datetime.utcnow)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship(Person)


class Transaction(Base):
    __tablename__ = 'transaction'
    # Here we define columns for the table Transaction.
    id = Column(Integer, primary_key=True)
    trade_amount = Column(Float, default=0)
    approved = Column(Boolean, default=False)
    deposit = Column(Float, default=0)
    from_account_id = Column(Integer, ForeignKey('account.id'))
    to_account_id = Column(Integer, ForeignKey('account.id'))
    tradetime = Column(DateTime, default=datetime.datetime.utcnow)
    from_account = relationship("Account", foreign_keys=[from_account_id])
    to_account = relationship("Account", foreign_keys=[to_account_id])


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///trade.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
