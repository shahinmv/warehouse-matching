from cProfile import label
from flask import Blueprint, render_template, request, flash, redirect, url_for
import requests
from db import db
from flask_login import login_required, current_user
from models.warehouse import Warehouse
import json

API_KEY = "AIzaSyDPYgtducg288JoPwZ3utMYUbKt_nxtAu4"

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html',)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@main.route('/admin')
@login_required
def admin():
    if current_user.isAdmin:
        data = Warehouse.query.order_by(Warehouse.id.asc()).all()
        return render_template('admin.html', data = data)
    else:
        return render_template('index.html')

@main.route('/admin', methods = ['POST'])
def admin_post():
    name = request.form.get('w_name')
    available_storage = request.form.get('w_astorage')
    total_storage = request.form.get('w_tstorage')

    labelling = True if request.form.getlist('labelling') else False
    manual_geo_data_entry = True if request.form.getlist('manual_geo_data_entry') else False
    item_packaging = True if request.form.getlist('item_packaging') else False
    palette_packaging = True if request.form.getlist('palette_packaging') else False

    address = request.form.get('address')
    email = request.form.get('email')
    phone = request.form.get('phone')

    new_warehouse = Warehouse(name, available_storage, total_storage, labelling, manual_geo_data_entry, item_packaging, palette_packaging, address, email, phone)

    db.session.add(new_warehouse)
    print("Added new warehouse")
    db.session.commit()
    print("Commited warehouse")
    flash('Added new warehouse.') 

    return redirect(url_for('main.admin'))

@main.route('/admin/<int:warehouse_id>')
@login_required
def warehouse_view(warehouse_id):
    data = Warehouse.query.filter_by(id=warehouse_id).one()

    return render_template('warehouse_view.html', data = data)

@main.route('/admin/<int:warehouse_id>', methods = ['POST'])
def admin_edit(warehouse_id):
    data = Warehouse.query.filter_by(id=warehouse_id).one()

    data.name = request.form.get("name")
    data.volume_available = request.form.get("a_volume")
    data.volume_total = request.form.get("t_volume")
    data.address = request.form.get("address")
    data.email = request.form.get("email")
    data.phone = request.form.get("phone")

    data.labelling = True if request.form.getlist('labelling') else False
    data.manual_geo_data_entry = True if request.form.getlist('manual_geo_data_entry') else False
    data.item_packaging = True if request.form.getlist('item_packaging') else False
    data.palette_packaging = True if request.form.getlist('palette_packaging') else False

    db.session.commit()
    return redirect(url_for('main.admin'))



@main.route('/test', methods=['POST'])
def test():
    position = request.get_json()
    result = json.loads(position)

    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="

    r = requests.get(url + str(result["latitude"]) + "," + str  (result["longitude"]) + "&key=" + API_KEY)

    print(r.json()["results"][1]["formatted_address"])
    
    return render_template('index.html', value = "Test")