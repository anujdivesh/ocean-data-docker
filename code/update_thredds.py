import requests
import xml.etree.ElementTree as xmltree
from owslib.wms import WebMapService
import pandas as pd
from controller_server_path import PathManager
from datetime import datetime, timedelta
import xarray as xr
import pandas as pd

class thredds:
    @staticmethod
    def get_data_from_api(url, params=None, headers=None):
        """
        Fetches data from a specified API endpoint.

        Args:
            url (str): The API endpoint URL.
            params (dict, optional): A dictionary of query parameters to send with the request.
            headers (dict, optional): A dictionary of HTTP headers to send with the request.

        Returns:
            dict or None: The JSON response from the API if successful, None otherwise.
        """
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

            return response.json()  # Return the JSON response as a dictionary
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    @staticmethod
    def update_api(url, data, headers=None):
        try:
            response1 = requests.post(PathManager.get_url('ocean-api',"token/"),json={"username":"admin","password":"Oceanportal2017*"})
            res1 = response1.json()
            token=headers={"Authorization":"Bearer "+res1['access']}
            response = requests.put(url+"/", json=data, headers=token)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()  # Return the response content as JSON
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
        except Exception as err:
            print(f"An error occurred: {err}")  # Handle other errors
        return None

    @staticmethod
    def get_6hourly(data):
        wms = WebMapService(data['url'], version="1.3.0")
        layer = data['layer_name']
        time = wms[layer].dimensions['time']['values'][0]
        start_time, end_time, period = time.split('/')

        #UPDATE API
        data2 = {"timeIntervalStart": start_time, "timeIntervalEnd": end_time}
        thredds.update_api(PathManager.get_url('ocean-api','layer_web_map',str(data['id'])), data2)
        print('Task '+ str(data['id']) +' : DateRange updated successsfully.')

        return None

    @staticmethod
    def get_specific(data):
        wms = WebMapService(data['url'], version="1.3.0")
        layer = data['layer_name']
        time = wms[layer].dimensions['time']['values']
        start_time = time[0]
        end_time = time[-1]

        #UPDATE API
        data2 = {"timeIntervalStart": start_time, "timeIntervalEnd": end_time}
        thredds.update_api(PathManager.get_url('ocean-api','layer_web_map',str(data['id'])), data2)
        print('Task '+ str(data['id']) +' : DateRange updated successsfully.')

        return None

    @staticmethod
    def get_specific_stamp(data):
        wms = WebMapService(data['url'], version="1.3.0")
        layer = data['layer_name']
        time = wms[layer].dimensions['time']['values']
        url = data['url']
        new_text = url.replace("wms", "dodsC")
        ds = xr.open_dataset(new_text)
        time_steps = ds['time'].values  # This retrieves the raw time values
        datetime_steps = pd.to_datetime(time_steps)
        datelist = []
        for dt in datetime_steps:
            datelist.append(dt)
        comma_separated_string = ', '.join(dt.strftime('%Y-%m-%dT%H:%M:%S') for dt in datelist)

        #UPDATE API
        data2 = {"specific_timestemps": comma_separated_string, "timeIntervalStart": datelist[0].isoformat(), "timeIntervalEnd": datelist[-1].isoformat()}
        #print(data2)
        thredds.update_api(PathManager.get_url('ocean-api','layer_web_map',str(data['id'])), data2)
        print('Task '+ str(data['id']) +' : DateRange updated successsfully.')

        return None

"""
#MAIN
api_url = PathManager.get_url('ocean-api',"layer_web_map/")
api_response = get_data_from_api(api_url)

for x in api_response:
    if x['update_thredds']:
        url = x['url']
        period = x['period']

        #CHECK EACH
        if period == 'COMMA':
            get_specific(x)
        elif period == 'PT6H':
            get_6hourly(x)
        elif period == 'P1D':
            get_6hourly(x)
        elif period == 'OPENDAP':
            get_specific_stamp(x)

"""
