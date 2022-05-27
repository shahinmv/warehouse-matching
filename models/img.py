from enum import unique
from db import db

class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.String(50))
    mimetype = db.Column(db.String(20))

    warehouse = db.Column(db.Integer)