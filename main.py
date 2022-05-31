from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
import requests
from db import db
from flask_login import login_required, current_user
from models.user import User
from werkzeug.utils import secure_filename

from models.warehouse import Warehouse
from models.warehouse_service import WarehouseServices
from models.img import Img


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', title = "Home")

@main.route('/dashboard/remove/<int:warehouse_id>')
def remove(warehouse_id):
    data = Warehouse.query.filter_by(id=warehouse_id).first()
    data_price = WarehouseServices.query.filter_by(warehouse_id=warehouse_id).first()

    if data_price:
        db.session.delete(data_price)
    
    db.session.delete(data)
    db.session.commit()

    return redirect(url_for('main.dashboard'))

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.isAdmin:
        data = Warehouse.query.order_by(Warehouse.id.asc()).all()
        users = User.query.all()
        return render_template('dashboard.html', data = data, users = users, title = "Dashboard")
    elif current_user.u_role == "owner":
        data = Warehouse.query.filter_by(owner = current_user.id).order_by(Warehouse.id.asc()).all()
        return render_template('dashboard.html', data = data, title = "Dashboard")
    else:
        abort(403) 

@main.route('/edit/details/<int:warehouse_id>')
@login_required
def warehouse_view(warehouse_id):
    if current_user.u_role == "owner" or current_user.isAdmin:
        data = Warehouse.query.filter_by(id=warehouse_id).one()
        if data.owner == current_user.id or current_user.isAdmin:
            return render_template('admin/warehouse_view.html', data = data, title = "Edit")
        else: 
            abort(403)
    else:
        abort(403)
 

@main.route('/edit/details/<int:warehouse_id>', methods = ['POST'])
def warehouse_edit(warehouse_id):
    data = Warehouse.query.filter_by(id=warehouse_id).first()
    w_price = WarehouseServices.query.filter_by(warehouse_id=warehouse_id).first()

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

    if w_price:
        if w_price.goods_receiving_labelling and not data.labelling:
            w_price.goods_receiving_labelling = None

        if w_price.goods_receiving_manuel_geo_data and not data.manual_geo_data_entry:
            w_price.goods_receiving_manuel_geo_data = None

        if w_price.item_packaging and not data.item_packaging:
            w_price.item_packaging = None

        if w_price.palette_packaging and not data.palette_packaging:
            w_price.palette_packaging = None

    db.session.commit()
    if current_user.isAdmin:
        return redirect(url_for('main.admin'))
    elif current_user.u_role == "owner":
        return redirect(url_for('main.dashboard'))

@main.route('/prices/<int:warehouse_id>')
@login_required
def warehouse_price(warehouse_id):
    if current_user.u_role == "owner" or current_user.isAdmin:
        data = Warehouse.query.filter_by(id=warehouse_id).one()
        if data.owner == current_user.id or current_user.isAdmin:
            data_price = WarehouseServices.query.filter_by(warehouse_id=warehouse_id).first()
            return render_template('admin/warehouse_price.html', data = data, data_price = data_price, title = "Prices")
        else:
            abort(403)
    else:
        abort(403)

@main.route('/prices/<int:warehouse_id>', methods = ['POST'])
def warehouse_price_Edit(warehouse_id):
    print("test")
    data = Warehouse.query.filter_by(id=warehouse_id).one()
    check = WarehouseServices.query.filter_by(warehouse_id=warehouse_id).first()

    if not check:
        storage = request.form.get("storage")
        item_picking = request.form.get("item_picking")
        packaging_material = request.form.get("packaging_material")
        goods_processing = request.form.get("goods_receiving_processing")

        new_wprice = WarehouseServices(storage, item_picking, goods_processing, packaging_material, warehouse_id)

        if data.labelling:
            new_wprice.set_labelling(request.form.get("goods_receiving_labelling"))

        if data.manual_geo_data_entry:
            new_wprice.set_manualgeodata(request.form.get("goods_receiving_manuel_geo_data"))

        if data.item_packaging:
            new_wprice.set_item(request.form.get("item_packaging"))

        if data.palette_packaging:
            new_wprice.set_packaging(request.form.get("palette_packaging"))
        
        db.session.add(new_wprice)
    else:
        check.storage = request.form.get("storage")
        check.item_picking = request.form.get("item_picking")
        check.packaging_material = request.form.get("packaging_material")
        check.goods_receiving_processing = request.form.get("goods_receiving_processing")


        if data.labelling:
            check.goods_receiving_labelling = request.form.get("goods_receiving_labelling")

        if data.manual_geo_data_entry:
            check.goods_receiving_manuel_geo_data = request.form.get("goods_receiving_manuel_geo_data")

        if data.item_packaging:
            check.item_packaging = request.form.get("item_packaging")

        if data.palette_packaging:
            check.palette_packaging = request.form.get("palette_packaging")

    db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/profile')
@login_required
def profile():
    if current_user.u_role == "owner":
        data = Warehouse.query.filter_by(owner = current_user.id).order_by(Warehouse.id.asc()).all()
        return render_template('profile.html', data = data, title = "Profile")
    else:
        return render_template('profile.html', title = "Profile")

@main.route('/add-warehouse')
@login_required
def add_warehouse():
    if current_user.u_role == "merchant":
        abort(403)
    elif current_user.u_role == "owner":
        return render_template('authentication/add_warehouse.html', title = "Add warehouse")

@main.route('/add-warehouse', methods = ['POST'])
def add_warehousePost():
    """ pic = request.files['pic']
    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    img = Img(img=pic.read(), name=filename, mimetype=mimetype, warehouse=current_user.id) """

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

    new_warehouse = Warehouse(name, available_storage, total_storage, labelling, manual_geo_data_entry, item_packaging, palette_packaging, address, email, phone, current_user.id)

    """ db.session.add(img) """
    db.session.add(new_warehouse)
    print("Added new warehouse")
    db.session.commit()
    print("Commited warehouse")

    return redirect(url_for('main.warehouse_price',warehouse_id = new_warehouse.id))


@main.route('/software')
def software():
    return render_template('software/software.html', title = "Under construction")


