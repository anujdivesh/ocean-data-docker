import requests
from datetime import datetime, timedelta
import netCDF4
import xarray as xr
from controller_country import initialize_countryController
import os
import shutil
from controller_server_path import PathManager
from dateutil.relativedelta import relativedelta
import calendar
from copernicusmarine import subset
import numpy as np

class Utility:
    @staticmethod
    def remove_substrings(original_string, substrings):
        for substring in substrings:
            original_string = original_string.replace(substring, "")
        return original_string
    
    @staticmethod
    def add_time(current_time, month=0, days=0, hours=0, minutes=0):
        new_time = current_time + timedelta(days=days, hours=hours, minutes=minutes)
        return new_time + relativedelta(months=month)
    
    @staticmethod
    def update_api(url, data, headers=None):
        try:
            response1 = requests.post(PathManager.get_url('ocean-api',"token/"),json={"username":"admin","password":"Oceanportal2017*"})
            res1 = response1.json()
            token=headers={"Authorization":"Bearer "+res1['access']}
            response = requests.put(url, json=data, headers=token)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()  # Return the response content as JSON
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
        except Exception as err:
            print(f"An error occurred: {err}")  # Handle other errors
        return None
    
    @staticmethod
    def url_exists(url):
        try:
            response = requests.head(url)
            # You can also use requests.get(url) if you need to access the content of the page
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            # Handle any exceptions that occur
            print(f"An error occurred: {e}")
            return False
        
    @staticmethod
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

    @staticmethod
    def time_diff(time1, time2):
        difference = time1 - time2
        difference_in_minutes = difference.total_seconds() / 60
        #print(difference_in_minutes)
        var = False
        #if abs(difference_in_minutes) > 0 and abs(difference_in_minutes) < 20:
        #    var = True
        if time2 < time1:
            var = True
        
        return var
    
    @staticmethod
    def get_subset(ds):
        subset_region = False
        if ds.subset == True:
            url = f"https://dev-oceanportal.spc.int/v1/api/country/%s" % (ds.subset_region)
            subset_region = initialize_countryController(url)
        return subset_region
    
    @staticmethod
    def subset_netcdf(ds, old_path, new_path):
        try:
            subset = xr.open_dataset(old_path)
            lon, lat = "", ""
            #CHECK IF DIMENSIONS ARE CORRECT
            for dim_name, dim in subset.dims.items():
                origname = dim_name.strip()
                tolower = origname.lower()
                if 'lon' in tolower:
                    lon = tolower
                if 'lat' in tolower:
                    lat = tolower
            
            #CHHECK IF VARIBLES IS REQUIRED
            if ds.has_variables:
                varib = ds.variables
                subset = subset[varib.split(",")]
            
            #CHECK IF SUBSET IS REQUIRED
            if ds.subset:
                #CHECK IF LON BETWEEN 0 TO 360
                below_zero = (subset[lon] < 0).any().values
                
                if below_zero:
                    first_part = subset.where(subset[lon] > 0, drop=True)
                    part_to_remove = subset.where(subset[lon] < 0, drop=True)
                    part_to_remove[lon] = (part_to_remove[lon] + 360) % 360
                    subset = xr.concat([first_part, part_to_remove], dim=lon)
                
                #CONTINUE SUBSETTING
                xmin_xmax = ds.xmin_xmax.strip()
                xmin_xmax_arr = xmin_xmax.split(',')
                ymin_ymax = ds.ymin_ymax.strip()
                ymin_ymax_arr = ymin_ymax.split(',')
                print(xmin_xmax_arr[0], xmin_xmax_arr[1], ymin_ymax_arr[0], ymin_ymax_arr[1])
                if lon.lower() == "lon":
                    subset = subset.sel(lat=slice(int(xmin_xmax_arr[0]), int(xmin_xmax_arr[1])),\
                                    lon=slice(int(ymin_ymax_arr[0]), int(ymin_ymax_arr[1])))
                else:
                    subset = subset.sel(latitude=slice(int(xmin_xmax_arr[0]), int(xmin_xmax_arr[1])),\
                                    longitude=slice(int(ymin_ymax_arr[0]), int(ymin_ymax_arr[1])))
            
            #SAVE NEW NETCDF
            subset  = xr.decode_cf(subset )
            subset.to_netcdf(path=new_path ,mode='w',format='NETCDF4',  engine='netcdf4')
            
            return True
        except Exception as e:
            return False
    
    @staticmethod
    def remove_file(url):
        if os.path.exists(url):
            os.remove(url)
        else:
            print("File was already removed.") 

    @staticmethod
    def rename_file(old_name, new_name):
        try:
            os.rename(old_name, new_name)
        except FileNotFoundError:
            print(f"File '{old_name}' not found.")
        except Exception as e:
            print(f"Error occurred: {e}")


    
    @staticmethod
    def update_tasks(download_succeed, is_error, new_file_name,new_download_time, task, ds):
        if download_succeed:
            data = {
                "next_run_time":new_download_time.strftime("%Y-%m-%d %H:%M:%S"),
                "last_run_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "next_download_file":new_file_name,
                "last_download_file":task.next_download_file,
                "success_count":task.success_count + 1,
                "health":"Excellent"
            }
            Utility.update_api(PathManager.get_url('ocean-api','task',str(task.id)), data)
            print('File download successful!')
        else:
            print('File does not exist, try again later')
            update_time = Utility.add_time(datetime.strptime(task.next_run_time,"%Y-%m-%dT%H:%M:%SZ"),ds.check_months,ds.check_days, ds.check_hours,ds.check_minutes).strftime("%Y-%m-%d %H:%M:%S")
            data = {
                "next_run_time":update_time,
                "last_run_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "attempt_count":task.attempt_count + 1,
                "health":"Poor"
            }
            Utility.update_api(PathManager.get_url('ocean-api','task',str(task.id)), data)

        if is_error:
            update_time = Utility.add_time(datetime.strptime(task.next_run_time,"%Y-%m-%dT%H:%M:%SZ"),ds.check_months,ds.check_days, ds.check_hours,ds.check_minutes).strftime("%Y-%m-%d %H:%M:%S")
            data = {
                    "next_run_time":update_time,
                    "last_run_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "fail_count":task.fail_count + 1,
                    "health":"Failed"
            }
            Utility.update_api(PathManager.get_url('ocean-api','task',str(task.id)), data)
            print('Download Failed')
        pass
    
    @staticmethod
    def copy_file(source_file, destination_file):
        try:
            shutil.copy(source_file, destination_file)
        except FileNotFoundError:
            print(f"Error: File '{source_file}' not found.")
        except PermissionError:
            print(f"Error: Permission denied to copy '{source_file}' to '{destination_file}'.")
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def get_first_last_day_of_month(year, month):
        """Returns the first day of the given month and year."""
        last_day = calendar.monthrange(year, month)[1]
        return datetime(year, month, 1), datetime(year, month, last_day)

    @staticmethod
    def download_from_copernicus(ds,dataset_id, varibales, start_datetime, end_datetime,new_file_name, download_directory):
        try:
            xmin_xmax = ds.xmin_xmax.strip()
            xmin_xmax_arr = xmin_xmax.split(',')
            ymin_ymax = ds.ymin_ymax.strip()
            ymin_ymax_arr = ymin_ymax.split(',')
            print(xmin_xmax_arr[0], xmin_xmax_arr[1], ymin_ymax_arr[0], ymin_ymax_arr[1])
            subset(
            dataset_id=dataset_id,
            variables=varibales,
            minimum_longitude= int(ymin_ymax_arr[0]),
            maximum_longitude= int(ymin_ymax_arr[1]),
            minimum_latitude= int(xmin_xmax_arr[0]),
            maximum_latitude= int(xmin_xmax_arr[1]),
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            force_download=True,
            overwrite_output_data=True,
            output_filename=new_file_name,
            output_directory=download_directory,
            credentials_file=PathManager.get_url('copernicus-credentials')
            )
            
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def get_last_sunday(year, month):
        # Find the last day of the month
        last_day_of_month = calendar.monthrange(year, month)[1]
        last_date_of_month = datetime(year, month, last_day_of_month)
        
        # Find the last Sunday of the month
        while last_date_of_month.weekday() != 6:  # 6 corresponds to Sunday
            last_date_of_month -= timedelta(days=1)
        
        return last_date_of_month

    @staticmethod
    def special_filename_coral_bleaching(prepare_new_time):
        #add 3 months
        new_date_time_months = prepare_new_time + relativedelta(months=4)
        #add 14 days
        new_date_time_obj = prepare_new_time + timedelta(days=14)
        lastSunday = Utility.get_last_sunday(new_date_time_months.year, new_date_time_months.month)

        return new_date_time_obj,lastSunday
    
    @staticmethod
    def subtract_special_one_month_coral(prepare_new_time):
        datetime_str = prepare_new_time.replace(".nc", "")
        new_date = datetime.strptime(datetime_str, "%Y%m%d")
        #add 3 months
        new_date_time_months = new_date + relativedelta(months=-1)
        lastSunday = Utility.get_last_sunday(new_date_time_months.year, new_date_time_months.month)

        return "%s.%s" % (lastSunday.strftime("%Y%m%d"), "nc")
    
    @staticmethod
    def reproject_netcdf(ds, old_path, new_path):
        try:
            subset = xr.open_dataset(old_path)
            lon, lat = "", ""
            #CHECK IF DIMENSIONS ARE CORRECT
            for dim_name, dim in subset.dims.items():
                origname = dim_name.strip()
                tolower = origname.lower()
                if 'lon' in tolower:
                    lon = tolower
                if 'lat' in tolower:
                    lat = tolower
            
            
            #CHECK IF LON BETWEEN 0 TO 360
            below_zero = (subset[lon] > 180).any().values

            if below_zero:
                print('converting from 0-360 to -180-180')
                lons = np.asarray(subset[lon].values)
                lons = (lons + 180) % 360 - 180
                subset[lon] = lons
                subset  = xr.decode_cf(ds )
                subset.to_netcdf(path=new_path ,mode='w',format='NETCDF4',  engine='netcdf4')
            
            return True
        except Exception as e:
            return False
    @staticmethod
    def download_obdaac(url, local_filename):
        try:
        # Send a GET request to the URL
            with requests.get(url, stream=True, timeout=120) as response:
                # Check if the request was successful
                response.raise_for_status()
                # Open a local file with the desired name
                with open(local_filename, 'wb') as file:
                    # Write the content to the file in chunks
                    #file.write(response.content)
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
            print(f"File downloaded as {local_filename}")
            return True
        except Exception as e:
            print(e)
            return False
            print('File not found.')