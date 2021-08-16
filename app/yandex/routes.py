from flask import request, render_template
import requests
from .env_var import *
import os
from . import yandex
from math import radians, cos, sin, asin, sqrt

# formula for calculate the distance between two points with latitude and longitude
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

apikey = os.environ.get('APIKEY')

msg = 'The location is inside the MKAD'

@yandex.route('/')
def index():
    return render_template('index.html')

@yandex.route('/result', methods=['POST'])
def yandex():

    # input field of html
    location1= request.form['location1']

    # url's for http request in yandex api developer
    url1 = 'https://geocode-maps.yandex.ru/1.x/?format=json&apikey='+apikey+'&geocode='+location1+'&lang=en-US'


    r1 = requests.get(url1).json()
    # Error handling
    if len(r1['response']['GeoObjectCollection']['featureMember']) == 0:

        return render_template('error.html')

    else:
        # Longitude and Latitude
        # Personal address points
        Points = r1['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']

        # Moscow  center Points
        lon_moscow_center = 37.621094
        lat_moscow_center = 55.753605

        # Personal address
        lon1, lat1 = Points.split()

        outside_mkad = haversine(float(lon1), float(lat1), lon_moscow_center, lat_moscow_center)

        if outside_mkad < 15:
            return render_template('results.html', results = msg)
        
        else:
            return render_template('results.html', results = outside_mkad)


# TODO: test file separate
# TODO: Documentation of haversine function
# TODO:  