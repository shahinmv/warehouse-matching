from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, current_app
from db import db
from models.warehouse import Warehouse
from models.warehouse_service import WarehouseServices
from flask_mail import Mail, Message

processes = Blueprint('processes', __name__)
mail = Mail()

@processes.route('/details/<int:warehouse_id>/request', methods=['POST'])
@login_required
def requestInfo(warehouse_id):
    flash("You will soon receive an email from us")

    msg = Message(subject="Your request", sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=[current_user.email])
    check = Warehouse.query.filter_by(id=warehouse_id).first()
    neededStorage = int(request.form.get('neededStorage'))
    if check.volume_available > neededStorage:
        msg.body = render_template('message/requestapprove.html', data = check)
    else:
        data = Warehouse.query.filter(Warehouse.volume_available>neededStorage).all()
        msg.body = render_template('message/requestdecline.html', unav = check, data = data)

    mail.send(msg)



    return redirect(url_for('main.details', warehouse_id=warehouse_id))