from flask import Flask
from flask_login import LoginManager
from auth import auth as auth_blueprint
from main import main as main_blueprint
from models.user import User
from models.warehouse import Warehouse
from models.warehouse_service import  WarehouseServices

from db import db

from main import main as main_blueprint
from auth import auth as auth_blueprint

app = Flask(__name__)

app.config['SECRET_KEY'] = 'shahin'

#   LOCAL DATABASE
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5000/thesis-db'
#   HEROKU HOSTED DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yqquhofwbxigmm:d2f6ddf9087969303f5eedf87b5e124060d4b25532ff0358f830b70ed9045b62@ec2-52-48-159-67.eu-west-1.compute.amazonaws.com:5432/d22qmtgc4978dh'

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.register_blueprint(main_blueprint)
app.register_blueprint(auth_blueprint)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5500, debug = True)