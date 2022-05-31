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
    
    locActive = request.form.get('closest_loc')
    print(locActive)
    

    filters = []
    words = name.split()

    if name:
        for n in words:
            search = "%{}%".format(n)
            filters.append(Warehouse.name.ilike(search))
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

        return render_template('search/filtersearch.html', title = 'Search', data = new_results, time = warehouse_d_t)
    else:
        return render_template('search/filtersearch.html', title = 'Search', data = results)

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
