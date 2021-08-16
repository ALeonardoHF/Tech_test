import requests
from .env_var import *
import os
from . import test
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

@test.route('/test')
def index():

    address_incorrect = 'Cathedral of the Intercession of the Most Holy Theotokos on the Moat'

    address_outside_mkad = 'Gorbunova Street, 14'

    address_inside_mkad = 'Partizanskaya Street, 20с2'

    # url = 'https://geocode-maps.yandex.ru/1.x/?format=json&apikey='+apikey+'&geocode='+address_incorrect+'&lang=en-US'
    # url = 'https://geocode-maps.yandex.ru/1.x/?format=json&apikey='+apikey+'&geocode='+address_inside_mkad+'&lang=en-US'
    url = 'https://geocode-maps.yandex.ru/1.x/?format=json&apikey='+apikey+'&geocode='+address_outside_mkad+'&lang=en-US'

    r = requests.get(url).json()

    if len(r['response']['GeoObjectCollection']['featureMember']) == 0:

        return 'Error, check the address'

    else:
        # Longitude and Latitude
        # Personal address points
        Points = r['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        # Personal address
        lon1, lat1 = Points.split()
        # Moscow  center Points
        lon_moscow_center = 37.621094
        lat_moscow_center = 55.753605

        outside_mkad = haversine(float(lon1), float(lat1), lon_moscow_center, lat_moscow_center)

        if outside_mkad < 15:
            print('The address is inside the MKAD')
            return 'The address is inside the MKAD'
        
        else:
            print(str(outside_mkad) + ' Kms')
            return 'Results: ' + str(outside_mkad) + ' Kms'