from email.policy import default
from db import db
from flask_login import UserMixin
import uuid

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    """ location = db.Column(db.String(100)) """
    u_role = db.Column(db.String(15))
    isAdmin = db.Column(db.Boolean, default=False)
    token = db.Column(db.String(255))

    def __init__(self, name, surname, email, password):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password

    def setToken(self):
        self.token = str(uuid.uuid4())

    """ def set_loc(self, loc):
        self.location = loc """
