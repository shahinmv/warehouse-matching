from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from models.user import User
from db import db

auth = Blueprint('auth', __name__)

@auth.route("/login")
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('loginName')
    password = request.form.get('loginPassword')
    remember = True if request.form.get('loginCheck') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page """
    
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('registerEmail')
    name = request.form.get('registerName')
    surname = request.form.get('registerSurname')
    password = request.form.get('registerPassword')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        print("true")
        return redirect(url_for('auth.signup'))

    new_user = User(name, surname, email, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    print("Added user")
    db.session.commit()
    print("Commited user")

    login_user(new_user)

    return redirect(url_for('main.profile'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))