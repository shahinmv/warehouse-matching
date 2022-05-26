from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from models.user import User

from db import db


auth = Blueprint('auth', __name__)

mail = Mail()



@auth.route("/login")
def login():
    return render_template('authentication/login.html', title = "Login")

@auth.route('/login', methods=['POST'])
def login_post():
    login = request.form.get('loginName')
    password = request.form.get('loginPassword')
    
    if "@" in login:
        email = login
        user = User.query.filter_by(email=email).first()
    else:
        username = login
        user = User.query.filter_by(username=username).first()

    remember = True if request.form.get('loginCheck') else False

    if not user or not check_password_hash(user.password, password):
        flash('Email address or password is incorrect')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page """
    
    login_user(user, remember=remember)
    if current_user.isAdmin:
        return redirect(url_for('main.dashboard'))
    else:
        return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('authentication/signup.html', title = "Sign up")

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('registerEmail')
    name = request.form.get('registerName')
    surname = request.form.get('registerSurname')
    role = request.form.get('inlineRadioOptions')
    username = request.form.get('registerUsername')
    password = request.form.get('registerPassword')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(name, surname, email, role, username, password=generate_password_hash(password, method='sha256'))
    new_user.setToken()

    db.session.add(new_user)
    print("Added user")
    db.session.commit()
    print("Commited user")

    login_user(new_user)

    if role == "owner":
        return redirect(url_for('main.add_warehouse'))
    else:
        return redirect(url_for('main.index'))

@auth.route("/forgot")
def forgot():
    return render_template('authentication/forgot.html', title = "Forgot")

@auth.route("/forgot", methods=['POST'])
def forgot_post():
    email = request.form.get('loginName')
    user = User.query.filter_by(email=email).first()
    if user:
        flash('Sent reset code to the email')
        user.setToken()

        msg = Message(subject="Forgot password request", sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=[email])
        msg.body = render_template("message/passwordreset.html", token = user.token, data = user)
        mail.send(msg)

        db.session.commit()
        return redirect(url_for('auth.forgot'))
    else:
        flash('Account with that email does not exist')
        return redirect(url_for('auth.forgot'))

@auth.route("/reset/<string:token>")
def reset(token):
    if not current_user.is_authenticated:
        return render_template('authentication/reset.html', token = token , title = "Reset password")
@auth.route("/reset/<string:token>", methods=['POST', 'GET'])
def reset_post(token):
    user = User.query.filter_by(token=token).first()
    print(url_for('auth.forgot'))
    if user:
        password = request.form.get("password")
        passwordConfirm = request.form.get("passwordConfirm")
        print(check_password_hash(user.password, password))

        if password != passwordConfirm:
            flash("Passwords do not match")
            return redirect(url_for('auth.reset', token = token))
        else:
            if check_password_hash(user.password, password):
                flash("You cant set your previous password")
                return redirect(url_for('auth.reset', token = token))
            else:
                flash("Password changed successfully")
                user.password = generate_password_hash(password, method='sha256')
                user.setToken()
                db.session.commit()
                return redirect(url_for('auth.login'))
    else:
        flash("Token not valid")
        return redirect(url_for('auth.forgot'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))