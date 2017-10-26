from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from db import Account, Base, Person, Transaction
from server import app,BaseHandler, MainHandler, LoginHandler, TransHandler, ApiHandler
from tornado import web, ioloop, gen, auth, escape
from tornado.testing import AsyncTestCase, gen_test, AsyncHTTPTestCase, AsyncHTTPClient
import unittest, os, os.path, sys, urllib
from tornado.options import options, define
from tornado.autoreload import watch
import json
import tornado


trackfile = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend/webpack-assets.json'))
engine = create_engine('sqlite:///trade.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

def clear_db():
    session.query(Account).filter_by(id=1).update({ Account.cur_amount: 1000})
    session.query(Account).filter_by(id=3).update({ Account.cur_amount: 2000})
    session.commit()



class ApiTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return app

    def test_login_get(self):
        response = self.fetch('/')
        self.assertEqual(response.code,200)

    # test login work with correct user
    def test_login_post(self):
        post_args = dict({'username': 'Jill', 'password':'Jill'})
        response = self.fetch('/', method="POST", body=urllib.urlencode(post_args), follow_redirects=False)
        self.assertEqual(response.code,302)
        self.assertTrue(response.headers['Location'] in './2')

    # test login work with incorrect user
    def test_login_post_incorrect(self):
        post_args = dict({'username': '111', 'password':'111'})
        response = self.fetch('/', method="POST", body=urllib.urlencode(post_args), follow_redirects=False)
        self.assertEqual(response.code,200)
        self.assertTrue('Try Again' in response.body)



    def test_api_login(self):
        post_args = dict({'username': 'Jill', 'password':'Jill'})
        response = self.fetch('/', method="POST", body=urllib.urlencode(post_args), follow_redirects=False)
        response = self.fetch(
                '/api',
                headers={'Cookie':response.headers['Set-Cookie']},
                )
        self.assertTrue('trade_amount' in response.body)
        self.assertEqual(response.code,200)


    def test_tran1(self):
        post_args = dict({'username': 'Jill', 'password':'Jill'})
        cookie_resp = self.fetch('/', method="POST", body=urllib.urlencode(post_args), follow_redirects=False)
        response = self.fetch(
                '/api',
                headers={'Cookie':cookie_resp.headers['Set-Cookie']},
                )
        data = json.loads(response.body)
        before_amount= float(data["trade_amount"])
        form_args = dict({'userid': '1', 'amount': '2000'})
        trans = self.fetch(
                '/trans', method="POST", body=urllib.urlencode(form_args),
                headers={'Cookie':cookie_resp.headers['Set-Cookie']},
                )
        response = self.fetch(
                '/api',
                headers={'Cookie':cookie_resp.headers['Set-Cookie']},
                )
        data_after = json.loads(response.body)
        after_amount = float(data_after["trade_amount"])
        self.assertEqual(before_amount-2000, after_amount)
        clear_db()

    def test_tran2(self):
        post_args = dict({'username': 'Jill', 'password':'Jill'})
        cookie_resp = self.fetch('/', method="POST", body=urllib.urlencode(post_args), follow_redirects=False)
        response = self.fetch(
                '/api',
                headers={'Cookie':cookie_resp.headers['Set-Cookie']},
                )
        data = json.loads(response.body)
        before_amount = float(data["trade_amount"])
        form_args = dict({'userid': '1', 'amount': '20000'})
        trans = self.fetch(
                '/trans', method="POST", body=urllib.urlencode(form_args),
                headers={'Cookie':cookie_resp.headers['Set-Cookie']},
                )
        response = self.fetch(
                '/api',
                headers={'Cookie':cookie_resp.headers['Set-Cookie']},
                )
        data_after = json.loads(response.body)
        after_amount = float(data_after["trade_amount"])
        self.assertEqual(before_amount, after_amount)
        clear_db()
    #
    def test_tran3(self):
        post_args = dict({'username': 'Jack', 'password':'Jack'})
        cookie_resp = self.fetch('/', method="POST", body=urllib.urlencode(post_args), follow_redirects=False)
        response = self.fetch(
                '/api',
                headers={'Cookie':cookie_resp.headers['Set-Cookie']},
                )
        data = json.loads(response.body)
        before_amount = float(data["trade_amount"])
        form_args = dict({'userid': '2', 'amount': '200'})
        trans = self.fetch(
                '/trans', method="POST", body=urllib.urlencode(form_args),
                headers={'Cookie':cookie_resp.headers['Set-Cookie']},
                )
        response = self.fetch(
                '/api',
                headers={'Cookie':cookie_resp.headers['Set-Cookie']},
                )
        data_after = json.loads(response.body)
        after_amount = float(data_after["trade_amount"])
        self.assertEqual(before_amount-200, after_amount)
        clear_db()




if __name__ == '__main__':
    with open(trackfile) as f:
        watch(trackfile)
        assets = json.load(f)
    define('ASSETS', assets)
    unittest.main()
