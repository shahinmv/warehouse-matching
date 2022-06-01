from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
import requests
from db import db
from flask_login import login_required, current_user
from models.warehouse import Warehouse
from models.warehouse_service import  WarehouseServices
from models.user import User
import json

API_KEY = "AIzaSyDPYgtducg288JoPwZ3utMYUbKt_nxtAu4"

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
    prices = WarehouseServices.query.all()

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

    #SERVICES PRICES
    labelling_min = request.form.get('labelling_price_min') 
    labelling_max = request.form.get('labelling_price_max') 

    manualgeo_min = request.form.get('manualgeo_price_min') 
    manualgeo_max = request.form.get('manualgeo_price_max') 

    itempackaging_min = request.form.get('itempackaging_price_min') 
    itempackaging_max = request.form.get('itempackaging_price_max') 

    palettepackaging_min = request.form.get('palettepackaging_price_min') 
    palettepackaging_max = request.form.get('palettepackaging_price_max')

    
    locActive = request.form.get('closest_loc')
    
    services = []
    filters = []
    words = name.split()

    if name:
        for n in words:
            search = "%{}%".format(n)
            filters.append(Warehouse.name.ilike(search))
    if n_storage:
        filters.append(Warehouse.volume_available >= n_storage)
    #FILTERING BASED ON SERVICES
    """ if labelling:
        filters.append(Warehouse.labelling.is_(True))
        services.append(Warehouse.labelling.is_(True))
        if labelling_min:
            filters.append(Warehouse.labelling_price >= labelling_min)
        if labelling_max:
            filters.append(Warehouse.labelling_price <= labelling_max)
        
    if manual_geo_data_entry:
        filters.append(Warehouse.manual_geo_data_entry.is_(True))
        if manualgeo_min:
            filters.append(Warehouse.manualgeo_price >= manualgeo_min)
        if manualgeo_max:
            filters.append(Warehouse.manualgeo_price <= manualgeo_max)

    if item_packaging:
        filters.append(Warehouse.item_packaging.is_(True))
        if itempackaging_min:
            filters.append(Warehouse.itempackaging_price >= itempackaging_min)
        if itempackaging_max:
            filters.append(Warehouse.itempackaging_price <= itempackaging_max)

    if palette_packaging:
        print("palette_packaging")
        filters.append(Warehouse.palette_packaging.is_(True))
        if palettepackaging_min:
            filters.append(Warehouse.palettepackaging_price >= palettepackaging_min)
        if palettepackaging_max:
            filters.append(Warehouse.palettepackaging_price <= palettepackaging_max) """
    temp_l = []
    if labelling:
        temp_l.append(Warehouse.labelling.is_(True))
        if labelling_min:
            temp_l.append(Warehouse.labelling_price >= labelling_min)
        if labelling_max:
            temp_l.append(Warehouse.labelling_price <= labelling_max)
        labelling_query = Warehouse.query.filter(db.and_(*temp_l)).all()
        print(labelling_query)

    temp_m = []
    if manual_geo_data_entry:
        temp_m.append(Warehouse.manual_geo_data_entry.is_(True))
        if labelling_min:
            temp_m.append(Warehouse.manualgeo_price >= manualgeo_min)
        if labelling_max:
            temp_m.append(Warehouse.manualgeo_price <= manualgeo_max)
        manualgeo_query = Warehouse.query.filter(db.and_(*temp_m)).all()
        print(manualgeo_query)

    z = list(set(labelling_query) - set(manualgeo_query))
    print(z)

    results = Warehouse.query.filter(db.and_(*filters)).all()
    print(results)

    if locActive:
        dicLoc = removeCharacters(locActive, '{":lattitudelongitude}')
        loc = getAddress(dicLoc)
        print(loc)
        warehouse_d_t = []

        for warehouses in results:
            temp = distanceMatrix(loc, warehouses.address)
            warehouse_d_t.append([warehouses.id, removeCharacters(temp["distance"]["text"], ",km "), temp["duration"]["text"]])

        warehouse_d_t.sort(key=lambda row: float(row[1]))

        new_results = []
        for warehouses in warehouse_d_t:
            for x in results:
                if x.id == warehouses[0]:
                    new_results.append(x)

        return render_template('search/filtersearch.html', title = 'Search', data = new_results, time = warehouse_d_t, prices = prices)
    else:
        return render_template('search/filtersearch.html', title = 'Search', data = results, prices = prices)

def getAddress(loc):
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="

    r = requests.get(url + str(loc[0]) + "," + str(loc[1]) + "&key=" + API_KEY)
    
    return r.json()["results"][1]["formatted_address"]

def distanceMatrix(loc, dest):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="

    r = requests.get(url + loc + "&destinations=" + dest + "&mode=car&key=" + API_KEY)
    
    return r.json()["rows"][0]["elements"][0]



def removeCharacters(input, chars):
    disallowed_characters = chars

    for character in disallowed_characters:
        input = input.replace(character, "")
    
    if "," in chars:
        return input
    else:
        return input.split(",")
