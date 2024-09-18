import netCDF4 as nc

# Step 1: Open the existing NetCDF file
input_file = 'http://opendap.bom.gov.au:8080/thredds/dodsC/nmoc/ww3_global_fc/ww3_20240707_12.G.nc'
src = nc.Dataset(input_file, 'r')

# Step 2: Create a new NetCDF file
output_file = 'output.nc'
dst = nc.Dataset(output_file, 'w', format='NETCDF4')

# Step 3: Copy global attributes
for name in src.ncattrs():
    dst.setncattr(name, src.getncattr(name))

# Step 4: Copy dimensions
for name, dimension in src.dimensions.items():
    dst.createDimension(name, (len(dimension) if not dimension.isunlimited() else None))

# Step 5: Copy variables and their attributes
for name, variable in src.variables.items():
    # Create the variable in the new file
    var = dst.createVariable(name, variable.datatype, variable.dimensions)
    
    # Copy variable attributes
    var.setncatts({k: variable.getncattr(k) for k in variable.ncattrs()})
    
    # Copy variable data
    var[:] = variable[:]

# Step 6: Close the NetCDF files
src.close()
dst.close()

print(f'Data and metadata have been successfully copied to {output_file}')