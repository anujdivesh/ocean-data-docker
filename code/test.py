import xarray as xr

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

subset = xr.open_dataset("http://tds.hycom.org/thredds/dodsC/GLBy0.08/expt_93.0/sur")
print(subset)


"""


# Example date
current_date = datetime.strptime("20240714", "%Y%m%d")

# Add 4 months using relativedelta
#new_date = current_date + relativedelta(months=4)
new_date = current_date + timedelta(days=140)  # Approximating 4 months as 30 days each

print(current_date, new_date)

subset = xr.open_dataset("/home/pop/Desktop/ocean-portal2.0/backend_design/AQUA_MODIS.20240201_20240229.L3m.MO.CHL.chlor_a.4km.NRT.nc")


subset = subset.sel(lat=slice(45, -45),lon=slice(100, 300))
subset.to_netcdf(path='/home/pop/Desktop/ocean-portal2.0/backend_design/test.nc' ,mode='w',format='NETCDF4',  engine='netcdf4')

def remove_attribute_from_variables(dataset, attribute_name):
    for var_name in dataset.variables:
        if attribute_name in dataset.variables[var_name].attrs:
            print('deleting')
            del dataset.variables[var_name].attrs[attribute_name]

subset = xr.open_dataset("/home/pop/Desktop/ocean-portal2.0/backend_design/AQUA_MODIS.20240201_20240229.L3m.MO.CHL.chlor_a.4km.NRT.nc")

subset = subset.sel(lat=slice(45, -45),lon=slice(100, 300))
subset  = xr.decode_cf(subset )


#varib = 'chlor_a'
#subset = subset[varib.split(",")]

remove_attribute_from_variables(subset, '_lastModified')

if '_lastModified' in subset.attrs:
    del subset.attrs['_lastModified']
#print(subset)
# List global attributes
print("\nGlobal attributes:")
for attr_name in subset.attrs:
    print(f"{attr_name}: {subset.attrs[attr_name]}")

# List variable-specific attributes
print("\nVariable attributes:")
for var_name in subset.variables:
    print(f"\nVariable: {var_name}")
    var_attrs = subset.variables[var_name].attrs
    for attr_name in var_attrs:
        print(f"    {attr_name}: {var_attrs[attr_name]}")


subset.to_netcdf(path='/home/pop/Desktop/ocean-portal2.0/backend_design/test.nc' ,mode='w',format='NETCDF4',  engine='netcdf4')

#subset.to_netcdf(path='/home/pop/Desktop/ocean-portal2.0/backend_design/test.nc' ,mode='w',format='NETCDF4',  engine='netcdf4')
"""