from flask import Blueprint, render_template
from db import db
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@main.route('/admin')
@login_required
def admin():
    if current_user.isAdmin:
        return render_template('admin.html')
    else:
        return render_template('index.html')