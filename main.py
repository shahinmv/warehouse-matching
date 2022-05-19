from flask import Blueprint, render_template, request
import requests
from db import db
from flask_login import login_required, current_user
import json

API_KEY = "AIzaSyDPYgtducg288JoPwZ3utMYUbKt_nxtAu4"

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@main.route('/admin')
@login_required
def admin():
    if current_user.isAdmin:
        return render_template('admin.html')
    else:
        return render_template('index.html')

@main.route('/test', methods=['POST'])
def test():
    position = request.get_json()
    result = json.loads(position)

    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="

    r = requests.get(url + str(result["latitude"]) + "," + str  (result["longitude"]) + "&key=" + API_KEY)

    print(r.json()["results"][1]["formatted_address"])
    
    return render_template('index.html', value = "Test")