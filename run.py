import os
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from auth import auth as auth_blueprint
from main import main as main_blueprint
from handlers import errors as errors_blueprint
from search import search as search_blueprint
from processes import processes as processes_blueprint
from models.user import User
from models.warehouse import Warehouse
from models.warehouse_service import  WarehouseServices
from models.warehouse_booking import  WarehouseBooking

from db import db

app = Flask(__name__, static_url_path='/static')
mail = Mail()

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

#   LOCAL DATABASE
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:<password>@localhost:5000/thesis-db'
#   DATABASE (set DATABASE_URL)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['GOOGLE_MAPS_API_KEY'] = os.environ.get('GOOGLE_MAPS_API_KEY', '')
app.register_blueprint(main_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(errors_blueprint)
app.register_blueprint(search_blueprint)
app.register_blueprint(processes_blueprint)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

db.init_app(app)
mail.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    app.run(port=5500, debug = True)