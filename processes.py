from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, current_app
from db import db
from models.user import User
from models.warehouse import Warehouse
from models.warehouse_service import WarehouseServices
from models.warehouse_booking import WarehouseBooking
from flask_mail import Mail, Message
from datetime import datetime

processes = Blueprint('processes', __name__)
mail = Mail()

@processes.route('/details/<int:warehouse_id>/test', methods=['POST'])
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

@processes.route('/details/<int:warehouse_id>/request', methods=['POST'])
@login_required
def requestBooking(warehouse_id):
    check = WarehouseBooking.query.filter(WarehouseBooking.merchant_id==current_user.id, WarehouseBooking.warehouse_id==warehouse_id).all()
    if check:
        flash("You already requested a booking")
        return redirect(url_for('search.details', warehouse_id = warehouse_id))
    n_storage = request.form.get('neededStorage')
    check_in = request.form.get('check-in')
    check_out = request.form.get('check-out')
    packaging_material = request.form.get('packaging_mat')

    receiving_processing = True if request.form.get('goods_receiving_processing_request') else False
    item_picking = True if request.form.get('item_picking_request') else False
    labelling = True if request.form.get('labelling_request') else False
    manual_geo = True if request.form.get('manual_geo_data_entry_request') else False
    item_packaging = True if request.form.get('item_packaging_request') else False

    warehouse = Warehouse.query.filter_by(id = warehouse_id).first()

    new_contract = WarehouseBooking(current_user.id, warehouse_id, n_storage, check_in, check_out, receiving_processing, item_picking, packaging_material, datetime.now())

    if warehouse.labelling:
        new_contract.set_labelling(labelling)
    if warehouse.manual_geo_data_entry:
        new_contract.set_manualgeo(manual_geo)
    if warehouse.item_packaging:
        new_contract.set_itempackaging(item_packaging)

    requestMailOwner(warehouse)
    requestMailMerchant(warehouse)
    db.session.add(new_contract)
    db.session.commit() 

    flash("Request has been sent. You will be notified by the warehouse owner soon")

    return redirect(url_for('search.details', warehouse_id = warehouse_id))

def requestMailOwner(warehouse):
    owner = User.query.filter_by(id = warehouse.owner).first()
    msg = Message(subject="Booking request", sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=[owner.email])
    msg.body = render_template('message/bookingrequestowner.html', owner = owner, merchant = current_user)
    mail.send(msg)

def requestMailMerchant(warehouse):
    msg = Message(subject="Booking request", sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=[current_user.email])
    msg.body = render_template('message/bookingrequestmerchant.html', merchant = current_user, data = warehouse)
    mail.send(msg)

@processes.route('/dashboard/delete/<int:booking_id>')
def reject(booking_id):
    booking = WarehouseBooking.query.filter(WarehouseBooking.id == booking_id).first()
    warehouse = Warehouse.query.filter(Warehouse.id == booking.warehouse_id).first()
    if current_user.id == warehouse.owner:
        if booking:
            booking.contracted = False
            db.session.commit()
            rejectMailMerchant(warehouse, booking)
        return redirect(url_for('main.dashboard'))
    else:
        abort(403)

def rejectMailMerchant(warehouse, booking):
    merchant = User.query.filter(User.id == booking.merchant_id).first()
    msg = Message(subject="Booking request rejected", sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=[merchant.email])
    msg.body = render_template('message/rejectmerchant.html', merchant = merchant, warehouse = warehouse)
    mail.send(msg)


@processes.route('/dashboard/accept/<int:booking_id>')
def accept(booking_id):
    booking = WarehouseBooking.query.filter(WarehouseBooking.id == booking_id).first()
    warehouse = Warehouse.query.filter(Warehouse.id == booking.warehouse_id).first()

    if current_user.id == warehouse.owner:
        if booking:
            booking.contracted = True
            db.session.commit()
            acceptMailMerchant(warehouse, booking)
        return redirect(url_for('main.dashboard'))
    else:
        abort(403)

def acceptMailMerchant(warehouse, booking):
    merchant = User.query.filter(User.id == booking.merchant_id).first()
    msg = Message(subject="Booking request accepted", sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=[merchant.email])
    msg.body = render_template('message/acceptmerchant.html', merchant = merchant, warehouse = warehouse)
    mail.send(msg)

@processes.route('/dashboard/active-bookings')
def view_bookings():
    bookings = []
    for x in current_user.warehouse_id:
        temp = WarehouseBooking.query.filter(WarehouseBooking.warehouse_id == x, WarehouseBooking.contracted == True).all()
        if temp:
            for item in temp:
                bookings.append(item)
    users = User.query.all()
    data = Warehouse.query.filter_by(owner = current_user.id).order_by(Warehouse.id.asc()).all()
    return render_template('activebookings.html', users = users, bookings = bookings, data = data)
       