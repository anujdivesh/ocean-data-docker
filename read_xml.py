import requests
import xml.etree.ElementTree as xmltree
from owslib.wms import WebMapService
import pandas as pd
# URL to the WMS GetCapabilities request
url = "http://localhost:8081/thredds/wms/POP/model/regional/copernicus/forecast/daily/salinity/latest.nc?service=WMS&version=1.3.0&request=GetCapabilities"



wms_url = 'http://localhost:8081/thredds/wms/POP/model/regional/copernicus/forecast/daily/salinity/latest.nc'

wms = WebMapService(wms_url, version="1.3.0")

print(wms['so'].dimensions['time'])

time_range_str = '2024-09-20T00:00:00.000Z/2024-09-27T00:00:00.000Z/P1D'

# Split the string to get start date, end date, and frequency
start_date, end_date, freq = time_range_str.split('/')

# Convert to a date range
date_range = pd.date_range(start=start_date, end=end_date, freq=freq)

# Convert to a list or array if needed
date_array = date_range.to_list()

print(date_array)