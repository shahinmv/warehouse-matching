from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
import requests
from db import db
from flask_login import login_required, current_user
from models.warehouse import Warehouse
from models.warehouse_service import  WarehouseServices
from models.user import User

search = Blueprint('search', __name__)

@search.route('/search')
def main():
    data = Warehouse.query.order_by(Warehouse.id.asc()).all()
    return render_template('search/search.html', title = "Search", data = data)

@search.route('/search/details/<int:warehouse_id>')
def details(warehouse_id):
    data = Warehouse.query.filter_by(id = warehouse_id).first()
    owner = User.query.filter_by(id = data.owner).first()
    return render_template('search/details.html', data = data, owner = owner, title = "Warehouse details")

@search.route('/search/filter', methods = ['POST'])
def filter():
    name = request.form.get('name')
    n_storage = request.form.get('n_storage')
    #MIN PRICE MAX PRICE
    min_p = request.form.get('min_p')
    max_p = request.form.get('max_p')
    #SERVICES
    labelling = True if request.form.get('labelling') else False
    manual_geo_data_entry = True if request.form.get('manual_geo_data_entry') else False
    item_packaging = True if request.form.get('item_packaging') else False 
    palette_packaging = True if request.form.get('palette_packaging') else False
    
    filters = []
    words = name.split()

    print(words)
    if name:
        for n in words:
            filters.append(Warehouse.name.match(n))
    if n_storage:
        filters.append(Warehouse.volume_available >= n_storage)
    #FILTERING BASED ON SERVICES
    if labelling:
        print("labelling")
        filters.append(Warehouse.labelling.is_(True))
    if manual_geo_data_entry:
        print("manual_geo_data_entry")  
        filters.append(Warehouse.manual_geo_data_entry.is_(True))
    if item_packaging:
        print("item_packaging")
        filters.append(Warehouse.item_packaging.is_(True))
    if palette_packaging:
        print("palette_packaging")
        filters.append(Warehouse.palette_packaging.is_(True))

    results = Warehouse.query.filter(db.and_(*filters)).all()

    return render_template('search/search.html', title = 'Search', data = results)
