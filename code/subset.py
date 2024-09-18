import xarray as xr
import matplotlib.pyplot as plt 
import numpy as np

#CHECK  IF WE HAVE TO CONVERT TO 0 TO 360
ds = xr.open_dataset('noaa-crw_mhw_v1.0.1_category_20240719.nc')
#ds = xr.open_dataset('combined.nc')

below_zero = (ds['lon'] < 0).any().values
if below_zero:
    first_part = ds.where(ds['lon'] > 0, drop=True)
    part_to_remove = ds.where(ds['lon'] < 0, drop=True)
    part_to_remove['lon'] = (part_to_remove['lon'] + 360) % 360
    ds = xr.concat([first_part, part_to_remove], dim='lon')

subset = ds.sel(lat=slice(-45, 45),\
                    lon=slice(100, 300))

subset  = xr.decode_cf(ds )
subset.to_netcdf(path='subset.nc' ,mode='w',format='NETCDF4',  engine='netcdf4')

"""
ds = xr.open_dataset('noaa-crw_mhw_v1.0.1_category_20240719.nc')

first_part = ds.where(ds['lon'] > 0, drop=True)

part_to_remove = ds.where(ds['lon'] < 0, drop=True)
part_to_remove['lon'] = (part_to_remove['lon'] + 360) % 360

combined_ds = xr.concat([first_part, part_to_remove], dim='lon')

combined_ds.to_netcdf(path='combined.nc' ,mode='w',format='NETCDF4',  engine='netcdf4')

combined = xr.open_dataset('combined.nc')
"""
#ds = xr.open_dataset('combined.nc')

# Plot one time step of the subset
#plt.figure(figsize=(10, 6))
#variable = combined_ds['heatwave_category']  # Replace with the actual variable name
#variable.isel(time=0).plot(cmap='viridis')
#plt.title('Subset of Data from THREDDS Server')
#plt.show()
# 
# 
#ds.close()
"""
min_lat = -45   # Minimum latitude
max_lat = 45   # Maximum latitude
min_lon = 100 # Minimum longitude
max_lon = 300 # Maximum longitude
subset = ds.sel(lat=slice(min_lat, max_lat), lon=slice(min_lon, max_lon))

#CHECK IF SUBSET IS REQUIRED
#if not ds.is_subset_auto:
#    subset_region = Utility.get_subset(ds)
#    subset = subset.sel(lat=slice(subset_region.north_bound_latitude, subset_region.south_bound_latitude),\
#                    lon=slice(subset_region.west_bound_longitude, subset_region.east_bound_longitude))

subset  = xr.decode_cf(subset )
subset.to_netcdf(path='subset2.nc' ,mode='w',format='NETCDF4',  engine='netcdf4')
"""