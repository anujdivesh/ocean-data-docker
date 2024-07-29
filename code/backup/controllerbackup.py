import json
from model_dataset import dataset
import requests
import xarray as xr
import matplotlib.pyplot as plt
import netCDF4 as nc
import numpy as np

class datasetController(dataset):
    def __init__(self, id, short_name, long_name, type,data_provider,data_source_url,data_download_url,login_credentials_required,username,\
                 password,API_key,download_method,download_file_prefix,download_file_infix,download_file_suffix,download_file_type,\
                    download_directory,download_frequency,subset,subset_region):
        super().__init__(id, short_name, long_name, type,data_provider,data_source_url,data_download_url,login_credentials_required,username,\
                 password,API_key,download_method,download_file_prefix,download_file_infix,download_file_suffix,download_file_type,\
                    download_directory,download_frequency,subset,subset_region)

    def dataDownload(self):
        if self.download_method == "opendap":
            variables_to_download = ['sig_wav_ht']
            min_lon = 100
            max_lon = 240
            min_lat = -45
            max_lat = 45

            print('downloading..')
            url = 'http://opendap.bom.gov.au:8080/thredds/fileServer/ww3_global_fc/ww3_20240511_00.G.nc'
            save_path = 'ww3.nc'
            download_large_file(url, save_path)
            #url = 'http://opendap.bom.gov.au:8080/thredds/dodsC/ww3_global_fc/ww3_20240708_00.G.nc'
            #ds = xr.open_dataset(url)
            #remove_attribute_from_variables(ds, '_Netcdf4Dimid')
            #ds = ds.assign_coords(longitude=((ds.lon + 360) % 360))
            ##subset = ds[variables_to_download]
            #subset = ds.sel(lat=slice(45, -45),lon=slice(100, 300))
            ##subset = ds.sel(lat=slice(min_lat, max_lat), lon=slice(min_lon, max_lon))
            ##subset.to_netcdf('3ww3_20240708_00.G.nc')
            #subset.to_netcdf(path= 'ww3.nc',mode='w', format='NETCDF4', engine='netcdf4')

            #file = nc.Dataset(fn)
            #lats = file.variables['lat'][:]
            #lons = file.variables['lon'][:]
            #latselect = np.logical_and(lats>min_lat,lats<max_lat)
            #lonselect = np.logical_and(lons>min_lon,lons<max_lon)
            #data = file.variables['sig_wav_ht'][0,latselect,lonselect]
            #print(latselect)
            #plt.contourf(data[::-1]) # flip latitudes so they go south -> north
            #plt.show()
            
            #ds = xr.open_dataset(fn)
            #lat_bnds, lon_bnds = [min_lat, max_lat], [min_lon, max_lon]
            #ds.sel(lat=slice(*lat_bnds), lon=slice(*lon_bnds))
            #ds.to_netcdf("test2assa2.nc")

            

            #f = nc.Dataset(fn, 'r+')
            #latbounds = [ min_lat , max_lat ]
            #lonbounds = [ min_lon , max_lon ] # degrees east ? 
            #lats = f.variables['lat'][:] 
            #lons = f.variables['lon'][:]

            ## latitude lower and upper index
            #latli = np.argmin( np.abs( lats - latbounds[0] ) )
            #latui = np.argmin( np.abs( lats - latbounds[1] ) ) 

            ## longitude lower and upper index
            #lonli = np.argmin( np.abs( lons - lonbounds[0] ) )
            #lonui = np.argmin( np.abs( lons - lonbounds[1] ) )  
            #airSubset = f.variables['sig_wav_ht'][ 0 , latli:latui , lonli:lonui ] 
            #print(airSubset)
            #plt.contourf(airSubset[0,:,:].T)
            #plt.colorbar()
            #ig = plt.figure()
            #ax=plt.pcolor(lons, lats, airSubset, cmap='viridis')#, vmin=min(Z[:]), vmax=max(Z))
            #plt.show()
            #dataset = xr.open_dataset(fn)
            ##dataset = dataset.assign_coords(lon=((dataset.lon + 360) % 360))
            #region_subset = dataset[variables_to_download]
            #region_subset = region_subset.sel(lat=slice(min_lat, max_lat),lon=slice(min_lon, max_lon))
            #region_subset2 = region_subset.rename({"sig_wav_ht":"sig"})
            #region_subset.to_netcdf("test2assa2.nc")
            #print(region_subset)

def initialize_datasetController(url):
    response = requests.get(url)
    if response.status_code == 200:
        item = response.json()
        dataset = datasetController(item['id'],item['short_name'], item['long_name'],item['type'], item['data_provider'],item['data_source_url'],\
                                item['data_download_url'],item['login_credentials_required'],item['username'],item['password'],\
                                item['API_key'],item['download_method'],item['download_file_prefix'],item['download_file_infix'],\
                                    item['download_file_suffix'],item['download_file_type'],item['download_directory'],\
                                        item['download_frequency'],item['subset'],item['subset_region'])
        return dataset
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

def download_large_file(url, destination):
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        print("File downloaded successfully!")
    except requests.exceptions.RequestException as e:
        print("Error downloading the file:", e)