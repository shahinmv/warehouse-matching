from db import db

class Ratings(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key = True)

    user_id = db.Column(db.Integer)
    warehouse_id = db.Column(db.Integer)
    score = db.Column(db.Float)

    def __init__(self, user_id, warehouse_id, score):
        self.user_id = user_id
        self.warehouse_id = warehouse_id
        self.score = score

        
