import json
from model_country import country
import requests
import xarray as xr
import netCDF4 as nc
import numpy as np

class countryController(country):
    def __init__(self, short_name, long_name, west_bound_longitude,east_bound_longitude,south_bound_latitude,north_bound_latitude):
        super().__init__(short_name, long_name, west_bound_longitude,east_bound_longitude,south_bound_latitude,north_bound_latitude)
            
def initialize_countryController(url):
    response = requests.get(url)
    if response.status_code == 200:
        item = response.json()
        dataset = countryController(item['short_name'], item['long_name'],item['west_bound_longitude'], item['east_bound_longitude'],\
                                    item['south_bound_latitude'], item['north_bound_latitude'])
        return dataset
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None