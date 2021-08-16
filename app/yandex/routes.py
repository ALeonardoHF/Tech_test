from flask import request
import json
from flask.templating import render_template
import requests
from .env_var import *
import os
from . import yandex
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km

client_id = os.environ.get('APPLICATION_ID')
client_secret = os.environ.get('APPLICATION_PASSWORD')
Url_callback = os.environ.get('URLCALLBACK')
apikey = os.environ.get('APIKEY')

# location1 = 'Partizanskaya Street, 20с2'
# location1 = 'Gorbunova Street, 14'

msg = 'The location is inside the MKAD'

@yandex.route('/')
def index():
    return render_template('index.html')

@yandex.route('/result', methods=['POST'])
def yandex():

    location1= request.form['location1']

    url1 = 'https://geocode-maps.yandex.ru/1.x/?format=json&apikey='+apikey+'&geocode='+location1+'&lang=en-US'
    moscow = 'https://geocode-maps.yandex.ru/1.x/?format=json&apikey='+apikey+'&geocode=37.6213676671642,55.7536532&lang=en-US'

    r1 = requests.get(url1).json()
    r3 = requests.get(moscow).json()

    # Longitude and Latitude
    # Personal address points
    Points1 = r1['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']

    # Moscow  center Points
    Points3 = r3['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']

    # Personal address
    lon1, lat1 = Points1.split()

    # Moscow center
    lon3, lat3 = Points3.split()

    outside_mkad = haversine(float(lon1), float(lat1), float(lon3), float(lat3))

    if outside_mkad < 15:
        return render_template('results.html', results = msg)
    
    else:
        return render_template('results.html', results = outside_mkad)
