import unittest
from flask_testing import TestCase
from seft_203_api.api import create_app as seft_203_create_app
from seft_203_api.db import db
from seft_203_api.models.user import UserModel
import requests
import json
import os
import sys

host = 'http://localhost:5000'

class MyTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://database.db"
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def create_app(self):
        app = seft_203_create_app(self)
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

        db.init_app(app)
        return app
    

    def setUp(self):
        db.create_all()
    
    def create_user_for_testing(self):

        data = {"username": "user", "password": "user", "full_name": "baovtnguyen"}
        self.client.post(f"{host}/auth/register", data=data)

    def test_register(self):

        data = {"username": "user", "password": "user", "full_name": "baovtnguyen"}
        response = self.client.post(f'{host}/auth/register', data=data)
        self.assertStatus(response, 201)  

    def test_login(self):
        
        self.create_user_for_testing()

        data = {"username": "user", "password": "user", "full_name": "baovtnguyen"}
        response = self.client.post(f'{host}/auth/login', data=data)
        self.assert200(response)


    # def test_logout(self):
    #     self.create_user()

    #     data = {"username": "user", "full_name": "baovtnguyen", "password": "user"}
    #     response = self.client.post(f'{host}/auth/login', data=data)
    #     self.assertStatus(response, 200)
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == "__main__":
    unittest.main(verbosity=2)