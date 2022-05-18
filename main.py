from flask import Blueprint, render_template
from db import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')