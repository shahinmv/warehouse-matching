from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
import requests
from db import db
from flask_login import login_required, current_user

search = Blueprint('search', __name__)

@search.route('/search')
def main():
    return render_template('search/search.html')