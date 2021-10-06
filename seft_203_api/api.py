from datetime import timedelta
from flask import Flask
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Api
from seft_203_api.resources.user import UserLogout
from seft_203_api.resources.user import UserRegister
from seft_203_api.resources.user import User
from seft_203_api.resources.user import UserLogin
from seft_203_api.resources.user import TokenRefresh

from seft_203_api.resources.dashboard import Dashboard
from seft_203_api.resources.dashboard import DashboardList

from seft_203_api.resources.task import Task
from seft_203_api.resources.task import TaskList
from seft_203_api.resources.task import TaskSearch

from seft_203_api.resources.contact import Contact
from seft_203_api.resources.contact import ContactList
from seft_203_api.resources.contact import ContactSearch

from seft_203_api.db import db
from seft_203_api.extensions import bcrypt
from seft_203_api.extensions import jwt

def create_app(config=None):
  
    ACCESS_EXPIRES = timedelta(minutes=30)
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    
    # app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/postgres"
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["JWT_SECRET_KEY"] = "super-secret-key"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

    api = Api(app)
    api.add_resource(UserLogin, "/auth/login")
    api.add_resource(UserLogout, "/auth/logout")
    api.add_resource(UserRegister, "/auth/register")
    api.add_resource(TokenRefresh, "/refresh")

    api.add_resource(Dashboard, "/dashboards/<string:dashboard_title>")
    api.add_resource(DashboardList, "/dashboards")

    api.add_resource(Task, "/tasks/<int:task_id>")
    api.add_resource(TaskList, "/tasks")
    api.add_resource(TaskSearch, "/searchtasks")

    api.add_resource(Contact, "/contacts/<int:contact_id>")
    api.add_resource(ContactList, "/contacts")
    api.add_resource(ContactSearch, "/searchcontacts")

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0')

