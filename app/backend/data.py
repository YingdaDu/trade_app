from sqlalchemy import create_engine, text
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from db import Account, Base, Person, Transaction

engine = create_engine('sqlite:///trade.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
# Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
#
#
person1 = Person(name='Jack', password="Jack")
person2 = Person(name='Jill', password="Jill")
session.add(person1)
session.add(person2)
session.commit()


jack1 = Account(cur_amount=1000, account_trade_amount=1000, person_id=1, isTrade=True)
jack2 = Account(cur_amount=1000, account_trade_amount=1000, person_id=1, isTrade=False)
session.add(jack1)
session.add(jack2)
jill1 = Account(cur_amount=2000, account_trade_amount=2000, person_id=2, isTrade=True)
jill2 = Account(cur_amount=2000, account_trade_amount=2000, person_id=2, isTrade=False)
session.add(jill1)
session.add(jill2)
session.commit()


df_person = pd.read_sql_query(
    text("SELECT * FROM Person"),
    engine
)
df_trade = pd.read_sql_query(
    text("SELECT * FROM Account WHERE Account.isTrade"),
    engine
)

df_check = pd.read_sql_query(
    text("SELECT * FROM Account WHERE NOT Account.isTrade"),
    engine
)
# print df_person
# print df_trade
# print df_check

t1 = Transaction(trade_amount=200, from_account_id=1, to_account_id=3, approved=True)
session.add(t1)
fromid= t1.from_account_id
toid = t1.to_account_id
session.query(Account).filter_by(id=fromid).update({Account.cur_amount: Account.cur_amount-t1.trade_amount})
session.query(Account).filter_by(id=toid).update({ Account.cur_amount: Account.cur_amount+t1.trade_amount})
session.commit()


# session.query(Transaction).delete()
# session.query(Account).filter_by(id=1).update({ Account.cur_amount: 1000})
# session.query(Account).filter_by(id=3).update({ Account.cur_amount: 2000})
# inst = inspect(Transaction)
# attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
# print(attr_names)
# inst = inspect(Account)
# attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
# print(attr_names)

# for i in session.query(Transaction).all():
#     print(i.approved)
#     print(i.deposit)
