from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Account, Base, Person, Transaction
import pandas as pd
import os
import json
import base64
import uuid
from tornado import web, ioloop, gen, auth, escape
from tornado.options import options, define
from tornado.autoreload import watch
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend/templates'))))
trackfile = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend/webpack-assets.json'))
engine = create_engine('sqlite:///trade.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

class BaseHandler(web.RequestHandler):
    def get_login_url(self):
        return "/"

    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        return user_json

    def get_database_session(self):
        return session

class MainHandler(BaseHandler):
    @web.authenticated
    def get(self):
        template = env.get_template('index.html')
        self.write(template.render({ 'assets': options.ASSETS }))



class LoginHandler(BaseHandler):
    def get(self):
        template = env.get_template('login.html')
        self.write(template.render({
            'assets': options.ASSETS
        }))

    def set_current_user(self, userid):
        if userid:
            self.set_secure_cookie("user", escape.json_encode(userid))
        else:
            self.clear_cookie("user")

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        session = self.get_database_session()
        auth = False
        userid = -1
        for i in session.query(Person).all():
            if (username == i.name and password == i.password):
                auth = True
                userid = i.id
        if auth:
            self.set_current_user(userid)
            self.redirect("/" + str(userid))
        else:
            error_msg = "The user is not registered"
            self.write("""

            <h3>The username or password is incorrect</h3>
            <form action="/" method="get"><button type="sumbit">Try Again</button></form>
            """)

class RegisterHandler(BaseHandler):
    def get(self):
        template = env.get_template('register.html')
        self.write(template.render({
            'assets': options.ASSETS
        }))


    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        check = float(self.get_argument("check", ""))
        trade = float(self.get_argument("trade", ""))
        if (username == "" or username == "" or check < 0 or trade < 0):
            self.render(os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend/templates/error.html')))
            return

        session = self.get_database_session()
        person = Person(name=username, password=password)
        session.add(person)
        session.commit()
        personid = person.id
        check = Account(cur_amount=check, account_trade_amount=check, person_id=personid, isTrade=False)
        trade = Account(cur_amount=trade, account_trade_amount=trade, person_id=personid, isTrade=True)
        session.add(check)
        session.add(trade)
        session.commit()
        self.redirect('/')



class TransHandler(BaseHandler):
    @web.authenticated
    def post(self):
        userid = str(self.get_argument("userid"))
        curid = str(self.get_current_user())
        amount = self.get_argument("amount")
        if amount.isdigit() and float(amount) > 0: #check the number is valid
            amount = float(amount)
        else:
            self.render(os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend/templates/error.html')))
            return

        session = self.get_database_session()
        #find the trade account id
        toid_q = "SELECT * FROM Account WHERE Account.person_id = %s AND Account.isTrade" %userid
        fromid_q = "SELECT * FROM Account WHERE Account.person_id = %s AND Account.isTrade" %curid
        df_to = pd.read_sql_query(toid_q, engine)
        df_from = pd.read_sql_query(fromid_q, engine)
        toid = df_to.loc[0][0]
        fromid = df_from.loc[0][0]
        total = 0
        for i in session.query(Account).filter_by(person_id=curid).all():
            total += i.cur_amount

        if (total > amount*0.2):
            t1 = Transaction(trade_amount=amount, approved=True, from_account_id=fromid, to_account_id=toid)
            session.add(t1)
            session.query(Account).filter_by(id=fromid).update({Account.cur_amount: Account.cur_amount - amount})
            session.query(Account).filter_by(id=toid).update({ Account.cur_amount: Account.cur_amount + amount})
            session.commit()
        else:
            desp = amount*0.2 - total + 1
            t1 = Transaction(trade_amount=amount, deposit=desp, from_account_id=fromid, to_account_id=toid)
            session.add(t1)
            session.commit()
        self.redirect('/' + self.get_secure_cookie("user"))



class ApiHandler(BaseHandler):
    @web.authenticated
    def get(self, *args):
        session = self.get_database_session()
        userid = self.get_current_user()
        query_user = "SELECT * FROM Person WHERE NOT Person.id = %s" %userid
        query_person = "SELECT * FROM Person WHERE Person.id = %s" %userid
        query_trade = "SELECT * FROM Account WHERE Account.person_id = %s AND Account.isTrade" %userid
        query_check = "SELECT * FROM Account WHERE Account.person_id = %s and NOT Account.isTrade" %userid
        df_person = pd.read_sql_query(query_person, engine)
        df_user = pd.read_sql_query(query_user,engine)
        df_trade = pd.read_sql_query(query_trade,engine)
        df_check = pd.read_sql_query(query_check,engine)
        namelist = zip(df_user.id, df_user.name)
        name = df_person.loc[0][1]
        trade_amount=df_trade.loc[0][1]
        check_amount=df_check.loc[0][1]
        trade_id = df_trade.loc[0][0]
        trans = []
        for i in session.query(Transaction).all():
            if (i.from_account_id==trade_id or i.to_account_id==trade_id):
                fpid=session.query(Account).filter_by(id=i.from_account_id).first().person_id
                from_name=session.query(Person).filter_by(id=fpid).first().name
                tpid=session.query(Account).filter_by(id=i.to_account_id).first().person_id
                to_name=session.query(Person).filter_by(id=tpid).first().name
                data = {
                        "approved": i.approved,
                        "deposit": i.deposit,
                        "id": i.id,
                        "from": from_name,
                        "to": to_name,
                        "trade_amount": i.trade_amount,
                        "time": str(i.tradetime)
                        }
                trans.append(data)


        metadata = {
            "namelist": namelist,
            "id": userid,
            "name": name,
            "trade_amount": trade_amount,
            "check_amount": check_amount,
            "trans": trans,
        }
        metadata = json.dumps(metadata)
        # print(metadata)
        self.write(metadata)
        self.set_header("Content-Type", "text/plain")
        self.finish()



app = web.Application([
        (r"/[0-9]+", MainHandler),
        (r'/api', ApiHandler),
        (r'/trans', TransHandler),
        (r'/', LoginHandler),
        (r'/register', RegisterHandler),
    ], static_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend/static')), debug=True,
    cookie_secret=base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes))


if __name__ == "__main__":
    try:
        with open(trackfile) as f:
            watch(trackfile)
            assets = json.load(f)
    except IOError:
        pass
    except KeyError:
        pass

    define('ASSETS', assets)
    app.listen(8888)
    ioloop.IOLoop.current().start()
