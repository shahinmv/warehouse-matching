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

from db import db

app = Flask(__name__)
mail = Mail()

app.config['SECRET_KEY'] = 'shahin'

#   LOCAL DATABASE
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5000/thesis-db'
#   HEROKU HOSTED DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fnqgcgvmozpmyl:f28265da2ca5f4fddc9de7e25e5cf8c7c06c95739d5d2ce3c4275d0fb3cc922f@ec2-54-76-43-89.eu-west-1.compute.amazonaws.com:5432/d1s5qe2312f8bg'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.register_blueprint(main_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(errors_blueprint)
app.register_blueprint(search_blueprint)
app.register_blueprint(processes_blueprint)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "fulfil.it.auto@gmail.com"
app.config['MAIL_DEFAULT_SENDER'] = "fulfil.it.auto@gmail.com"
app.config['MAIL_PASSWORD'] = 'Shahin2001'
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