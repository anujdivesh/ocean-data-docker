import xarray as xr
import numpy as np
import pandas as pd
import os
import glob
 
# List of variables to keep (ensure these match your actual NetCDF file's variable names)
variables_to_keep = ['hs', 'dir', 'latitude', 'longitude', 't0m1', 'time']
 
# Directory containing the original files (adjust the path as necessary)
file_directory = r"S:\\GEM\\FJ_NAB\\O_M\\Oceans\\Original_Sources\\PACCSAP_WAVE_HINDCAST_DATA\\GRIDDED\\GLOB\\ww3.glob_24m.*.nc"
 
# Output directory for converted data
output_directory = r"C:\\Users\\MoleniT\\test_data_nc4"
 
# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
 
# Function to find the nearest coordinate value in a range
def find_nearest(array, value):
    idx = (np.abs(array - value)).argmin()
    return array[idx]
 
# Process files from 2019 to 2023
years_to_process = range(2016, 2024)
 
for file in glob.glob(file_directory):
    # Extract the file name without the directory path
    file_name = os.path.basename(file)
    # Check if the file name includes one of the years we want to process
    if not any(str(year) in file_name for year in years_to_process):
        continue
    # Define the output file path for .nc4 format
    output_file_name = os.path.splitext(file_name)[0] + ".nc4"
    output_file_path = os.path.join(output_directory, output_file_name)
    try:
        # Open the NetCDF file
        ds = xr.open_dataset(file)
        # Check if the specified variables are in the dataset
        missing_vars = [var for var in variables_to_keep if var not in ds.variables]
        if missing_vars:
            print(f"File {file} is missing variables: {missing_vars}")
            continue
        # Select the variables of interest
        ds_selected = ds[variables_to_keep]
        # Rename 't0m1' to 'Tm' if it exists
        if 't0m1' in ds_selected:
            ds_selected = ds_selected.rename({'t0m1': 't'})
        # Convert the time to datetime objects if it's not already
        if not pd.api.types.is_datetime64_any_dtype(ds_selected['time']):
            try:
                units = ds_selected['time'].attrs['units']
                reference_time = pd.to_datetime(units.split('since ')[1].strip())
                ds_selected['time'] = reference_time + pd.to_timedelta(ds_selected['time'].values, unit='D')
            except Exception as e:
                print(f"Failed to convert time for file {file}: {e}")
                continue
        # Filter by the specified year range (2019 to 2023)
        ds_filtered = ds_selected.sel(time=slice('2016-01-01', '2023-12-31'))
        # Check latitude and longitude ranges
        lat_min, lat_max = ds_filtered.latitude.min(), ds_filtered.latitude.max()
        lon_min, lon_max = ds_filtered.longitude.min(), ds_filtered.longitude.max()
        # Select the nearest latitude and longitude points within the desired range
        lat_min_nearest = find_nearest(ds_filtered.latitude.values, 46)
        lat_max_nearest = find_nearest(ds_filtered.latitude.values, -46)
        lon_min_nearest = find_nearest(ds_filtered.longitude.values, 100)
        lon_max_nearest = find_nearest(ds_filtered.longitude.values, 300)
 
        print(f"Selected Latitude range: {lat_max_nearest} to {lat_min_nearest}")
        print(f"Selected Longitude range: {lon_min_nearest} to {lon_max_nearest}")
        # Apply the nearest latitude and longitude boundaries
        ds_filtered = ds_filtered.sel(latitude=slice(lat_max_nearest, lat_min_nearest))
        ds_filtered = ds_filtered.sel(longitude=slice(lon_min_nearest, lon_max_nearest))
 
        # Save the filtered data to .nc4 format
        ds_filtered.to_netcdf(output_file_path, format='NETCDF4', mode='w', engine='netcdf4')
        print(f"Converted and saved to .nc4: {output_file_path}")
    except Exception as e:
        print(f"Failed to process file {file}: {e}")
        continue
 