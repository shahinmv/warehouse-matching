from flask import Flask
from db import db

from main import main as main_blueprint

app = Flask(__name__)

app.config['SECRET_KEY'] = 'shahin'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5000/thesis-db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.register_blueprint(main_blueprint)

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5500, debug = True)