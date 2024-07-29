import xarray as xr
import matplotlib.pyplot as plt
 
 
def remove_attribute_from_variables(dataset, attribute_name):
    for var_name in dataset.variables:
        if attribute_name in dataset.variables[var_name].attrs:
            del dataset.variables[var_name].attrs[attribute_name]
 
 
file = 'http://opendap.bom.gov.au:8080/thredds/dodsC/ww3_global_fc/ww3_20240708_00.G.nc'
 
da = xr.open_dataset(file)
 
 
# Remove the  fucking'_Netcdf4Dimid' attribute from variables
remove_attribute_from_variables(da, '_Netcdf4Dimid')
 
 
subset = da.sel(lat=slice(-15.5, -19.5), 
                     lon=slice(175, 184))
 
 
# List global attributes
print("\nGlobal attributes:")
for attr_name in da.attrs:
    print(f"{attr_name}: {subset.attrs[attr_name]}")
 
# List variable-specific attributes
print("\nVariable attributes:")
for var_name in da.variables:
    print(f"\nVariable: {var_name}")
    var_attrs = subset.variables[var_name].attrs
    for attr_name in var_attrs:
        print(f"    {attr_name}: {var_attrs[attr_name]}")
 
 
"""
variable_names = list(subset.variables.keys())

 
variable_name = 'sig_wav_ht'  # Replace with the actual variable name
time_step = subset.isel(time=0)  # Select the first time step
 
data = time_step[variable_name].values
lat = time_step['lat'].values
lon = time_step['lon'].values
 
 
plt.figure(figsize=(10, 6))
plt.pcolor(lon, lat, data, shading='auto')  # Use shading='auto' to avoid warnings about pcolor
plt.colorbar(label=f'{variable_name} values')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title(f"{variable_name} at time step {time_step['time'].values}")
plt.show()
"""
 
# Save the subsetted dataset to a local NetCDF file
subset.to_netcdf('subsetted_data.nc')