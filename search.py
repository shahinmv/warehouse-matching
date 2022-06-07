from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
import requests
from db import db
from flask_login import login_required, current_user
from models.warehouse import Warehouse
from models.warehouse_service import  WarehouseServices
from models.warehouse_booking import WarehouseBooking
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
    check = WarehouseBooking.query.filter(WarehouseBooking.merchant_id==current_user.id, WarehouseBooking.warehouse_id==warehouse_id).first()
    return render_template('search/details.html', data = data, owner = owner, check = check, title = "Warehouse details")

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

    if labelling_min:
        print("true")

    
    locActive = request.form.get('closest_loc')
    
    services = [labelling, manual_geo_data_entry, item_packaging, palette_packaging]
    filters = []
    words = name.split()

    if name:
        for n in words:
            search = "%{}%".format(n)
            filters.append(Warehouse.name.ilike(search))
    if n_storage:
        filters.append(Warehouse.volume_available >= n_storage)
    
    #results = Warehouse.query.filter(db.and_(*filters)).all()
    #FILTERING BASED ON SERVICES
    results = []
    labelling_difference = []
    manualgeo_difference = []
    itempackaging_difference = []
    palettepackaging_difference = []
    filter_prices = {}
    filter_prices_bool = {}

    if labelling:
        temp_l = filters.copy()
        temp_l.append(Warehouse.labelling.is_(True))
        if labelling_min:
            temp_l.append(Warehouse.labelling_price >= labelling_min)
            filter_prices['labelling_min'] = int(labelling_min)
            filter_prices_bool['labelling_min'] = True
        else:
            filter_prices_bool['labelling_min'] = False
        if labelling_max:
            temp_l.append(Warehouse.labelling_price <= labelling_max)
            filter_prices['labelling_max'] = int(labelling_max)
            filter_prices_bool['labelling_max'] = True
        else:
            filter_prices_bool['labelling_max'] = False
        labelling_query = Warehouse.query.filter(db.and_(*temp_l)).all()

        results = results + labelling_query

    if manual_geo_data_entry:
        temp_m = filters.copy()
        temp_m.append(Warehouse.manual_geo_data_entry.is_(True))
        if manualgeo_min:
            temp_m.append(Warehouse.manualgeo_price >= manualgeo_min)
            filter_prices['manualgeo_min'] = int(manualgeo_min)
            filter_prices_bool['manualgeo_min'] = True
        else:
            filter_prices_bool['manualgeo_min'] = False
        if manualgeo_max:
            temp_m.append(Warehouse.manualgeo_price <= manualgeo_max)
            filter_prices['manualgeo_max'] = int(manualgeo_max)
            filter_prices_bool['manualgeo_max'] = True
        else:
            filter_prices_bool['manualgeo_max'] = False
        manualgeo_query = Warehouse.query.filter(db.and_(*temp_m)).all()
        if labelling and labelling_difference:
            manualgeo_difference = list(set(manualgeo_query) - set(labelling_difference))
        else:
            manualgeo_difference = list(set(manualgeo_query) - set(results))

        results = results + manualgeo_difference

    if item_packaging:
        temp_i = filters.copy()
        temp_i.append(Warehouse.item_packaging.is_(True))
        if itempackaging_min:
            temp_i.append(Warehouse.itempackaging_price >= itempackaging_min)
            filter_prices['item_min'] = int(itempackaging_min)
            filter_prices_bool['item_min'] = True
        else:
            filter_prices_bool['item_min'] = False
        if itempackaging_max:
            temp_i.append(Warehouse.itempackaging_price <= itempackaging_max)
            filter_prices['item_max'] = int(itempackaging_max)
            filter_prices_bool['item_max'] = True
        else:
            filter_prices_bool['item_max'] = False
        itempackaging_query = Warehouse.query.filter(db.and_(*temp_i)).all()
        if manual_geo_data_entry and manualgeo_difference:
            itempackaging_difference = list(set(itempackaging_query) - set(manualgeo_difference))
        elif labelling and labelling_difference:
            itempackaging_difference = list(set(itempackaging_query) - set(labelling_difference))
        else:
            itempackaging_difference = list(set(itempackaging_query) - set(results))
        
        results = results + itempackaging_difference

    if palette_packaging:
        temp_p = filters.copy()
        temp_p.append(Warehouse.palette_packaging.is_(True))
        if palettepackaging_min:
            temp_p.append(Warehouse.palettepackaging_price >= palettepackaging_min)
            filter_prices['palette_min'] = int(palettepackaging_min)
            filter_prices_bool['palette_min'] = True
        else:
            filter_prices_bool['palette_min'] = False
        if palettepackaging_max:
            temp_p.append(Warehouse.palettepackaging_price <= palettepackaging_max)
            filter_prices['palette_max'] = int(palettepackaging_max)
            filter_prices_bool['palette_max'] = True
        else:
            filter_prices_bool['palette_max'] = False
        palettepackaging_query = Warehouse.query.filter(db.and_(*temp_p)).all()
        if item_packaging and itempackaging_difference:
            palettepackaging_difference = list(set(palettepackaging_query) - set(itempackaging_difference))
        elif manual_geo_data_entry and manualgeo_difference:
            palettepackaging_difference = list(set(palettepackaging_query) - set(manualgeo_difference))
        elif labelling and labelling_difference:
            palettepackaging_difference = list(set(palettepackaging_query) - set(labelling_difference))
        else:
            palettepackaging_difference = list(set(palettepackaging_query) - set(results))
        
        results = results + palettepackaging_difference
    
    if not labelling and not manual_geo_data_entry and not item_packaging and not palette_packaging:
        results = Warehouse.query.filter(db.and_(*filters)).all()

        
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

        return render_template('search/filtersearch.html', title = 'Search', data = new_results, time = warehouse_d_t, prices = prices, services = services, filter_prices = filter_prices, filter_prices_bool = filter_prices_bool)
    else:
        return render_template('search/filtersearch.html', title = 'Search', data = results, prices = prices, services = services, filter_prices = filter_prices, filter_prices_bool = filter_prices_bool)

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
