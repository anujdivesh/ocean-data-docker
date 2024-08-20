
from model_task import task
from controller_dataset import initialize_datasetController
from controller_country import initialize_countryController
import requests
from datetime import datetime, timedelta
from utility_functions import Utility
from controller_server_path import PathManager
import subprocess
import os, sys
import netCDF4
import xarray as xr
from copernicusmarine import subset

class taskController(task):
    def __init__(self, id, task_name, class_id, dataset_id,status,priority,\
                 duration,task_start_time,next_run_time,last_run_time,next_download_file,last_download_file,enabled,health,fail_count,\
                    success_count,reset_count,attempt_count,predecessor_class,predecessor_class_id,successor_class,successor_class_id,created_by,launched_by,\
                        retain,retention_days):
        super().__init__( id, task_name, class_id, dataset_id,status,priority,\
                 duration,task_start_time,next_run_time,last_run_time,next_download_file,last_download_file,enabled,health,fail_count,\
                    success_count,reset_count,attempt_count,predecessor_class,predecessor_class_id,successor_class,successor_class_id,created_by,launched_by,\
                        retain,retention_days)
    
    def generate_current_download_time(self,ds):
        convert_to_datetime = ""
        suffix = ds.download_file_suffix
        if "{special}" in suffix:
            substrings_to_remove = [ds.download_file_prefix, ".nc"]
            new_string = Utility.remove_substrings(self.next_download_file, substrings_to_remove)
            seperate = new_string.split("_")
            convert_to_datetime = datetime.strptime(seperate[0], ds.download_file_infix)
        else:
            substrings_to_remove = [ds.download_file_prefix, ds.download_file_suffix]
            new_string = Utility.remove_substrings(self.next_download_file, substrings_to_remove)
            convert_to_datetime = datetime.strptime(new_string, ds.download_file_infix)

        return convert_to_datetime

    #GENERATE NEXT DOWNLOAD FILENAME AND NEXT DOWNLOAD TIME
    def generate_next_download_filename(self,ds):
        new_file_name,new_download_time = "",""
        suffix = ds.download_file_suffix
        if "{special}" in suffix:
            print('Special file name generation...')
            substrings_to_remove = [ds.download_file_prefix, ".nc"]
            new_string = Utility.remove_substrings(self.next_download_file, substrings_to_remove)
            seperate = new_string.split("_")
            convert_to_datetime = datetime.strptime(seperate[0], ds.download_file_infix)
            prepare_new_time = Utility.add_time(convert_to_datetime,ds.frequency_months,ds.frequency_days, ds.frequency_hours,ds.frequency_minutes)
            first_date, second_date = Utility.special_filename_coral_bleaching(prepare_new_time)
            new_file_name = ds.download_file_prefix+prepare_new_time.strftime('%Y%m%d')+"_for_"+first_date.strftime('%Y%m%d')+"to"+second_date.strftime('%Y%m%d')+".nc"
            new_download_time = Utility.add_time(prepare_new_time,ds.check_months,ds.check_days, ds.check_hours,ds.check_minutes)
        else:
            if ds.download_file_infix.strip() == "":
                new_file_name = self.next_download_file
                prepare_new_time = datetime.strptime(self.next_run_time, "%Y-%m-%dT%H:%M:%SZ")
                new_download_time = Utility.add_time(prepare_new_time,ds.check_months,ds.check_days, ds.check_hours,ds.check_minutes)

            else:
                substrings_to_remove = [ds.download_file_prefix, ds.download_file_suffix]
                new_string = Utility.remove_substrings(self.next_download_file, substrings_to_remove)

                if "_" in new_string:
                    print("extreme datetime")
                    date_split = new_string.split('_')
                    infix_split = ds.download_file_infix.split('_')
                    convert_to_datetime = datetime.strptime(date_split[0], infix_split[0])
                    prepare_new_time = Utility.add_time(convert_to_datetime,ds.frequency_months,ds.frequency_days, ds.frequency_hours,ds.frequency_minutes)
                    
                    if ds.download_method == 3:
                        new_file_name = ds.download_file_prefix + "" +prepare_new_time.strftime(infix_split[0]) +"_"+prepare_new_time.strftime(infix_split[1])+ ds.download_file_suffix
                        new_download_time = Utility.add_time(prepare_new_time,ds.check_months,ds.check_days, ds.check_hours,ds.check_minutes)
                    elif ds.download_method == 2: 
                        first_day,last_day = Utility.get_first_last_day_of_month(prepare_new_time.year, prepare_new_time.month)
                        new_file_name = ds.download_file_prefix + "" +first_day.strftime(infix_split[0]) +"_"+last_day.strftime(infix_split[1])+ ds.download_file_suffix
                        new_download_time = Utility.add_time(first_day,ds.check_months,ds.check_days, ds.check_hours,ds.check_minutes)
                    else:
                        convert_to_datetime = datetime.strptime(new_string, ds.download_file_infix)
                        prepare_new_time = Utility.add_time(convert_to_datetime,ds.frequency_months,ds.frequency_days, ds.frequency_hours,ds.frequency_minutes)
                        new_file_name = ds.download_file_prefix + "" +prepare_new_time.strftime(ds.download_file_infix) + ds.download_file_suffix
                        new_download_time = Utility.add_time(prepare_new_time,ds.check_months,ds.check_days, ds.check_hours,ds.check_minutes)

                else:
                    print("normal datetime")
                    convert_to_datetime = datetime.strptime(new_string, ds.download_file_infix)
                    prepare_new_time = Utility.add_time(convert_to_datetime,ds.frequency_months,ds.frequency_days, ds.frequency_hours,ds.frequency_minutes)
                    new_file_name = ds.download_file_prefix + "" +prepare_new_time.strftime(ds.download_file_infix) + ds.download_file_suffix
                    new_download_time = Utility.add_time(prepare_new_time,ds.check_months,ds.check_days, ds.check_hours,ds.check_minutes)
            
        return new_file_name,new_download_time

    #CORAL BLEACHING HAS ISSUES SOMETIMES 
    def try_multiple_only_coral(self,ds,url):
        exists = Utility.url_exists(url)
        
        print('trying multiple')
        suffix = ds.download_file_suffix
        new_url = url
        if not exists:
            if "{special}" in suffix:
                split = url.split("to")
                #print(split[1])
                last = Utility.subtract_special_one_month_coral(split[1])
                new_url = url.replace(split[1], last)
                print("new url: "+new_url)
        return new_url


    def create_product_directory(self,ds):
        local_dir = ds.local_directory_path
        root_dir = PathManager.get_url('root-dir')
        if "{root-dir}" in local_dir:
            local_dir = local_dir.replace("{root-dir}", root_dir)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        pass

    def download_http(self,ds):
        download_complete = False
        is_error = False
        try:
            #GET URL
            url = ds.data_download_url
            
            #CHECK FOR YEAR
            if "{year}" in url:
                convert_to_datetime = self.generate_current_download_time(ds)
                url = url.replace('{year}', convert_to_datetime.strftime('%Y'))

            #CHECK FOR MONTH
            if "{month}" in url:
                convert_to_datetime = self.generate_current_download_time(ds)
                url = url.replace('{month}', convert_to_datetime.strftime('%m'))
            
            #REPLACE WITH FILE TO DOWNLOAD
            if "{download_file_name}" in url:
                url = url.replace('{download_file_name}', self.next_download_file)
            

            #TRY MULTIPLE FOR CORAL
            suffix = ds.download_file_suffix
            if "{special}" in suffix:
                url = self.try_multiple_only_coral(ds,url)

            print(url)

            if Utility.url_exists(url):
                #DOWNLOAD THE FILE
                Utility.download_large_file(url,PathManager.get_url('tmp',self.next_download_file))
                
                #RENAME TO TMP IN THE SAME DIR
                tmp_name = "%s%s" % (PathManager.get_url('tmp',self.next_download_file), "_tmp.nc")
                Utility.rename_file(PathManager.get_url('tmp',self.next_download_file), tmp_name)
                
                
                #IF SUBSET OR VARIBLES
                if ds.has_variables or ds.subset:
                    print('subsetting')
                    output_file = "%s" % (PathManager.get_url('tmp',self.next_download_file))
                    is_subsetted = Utility.subset_netcdf(ds, tmp_name, output_file)
                    if not is_subsetted:
                        Utility.rename_file(tmp_name,PathManager.get_url('tmp',self.next_download_file))

                else:
                    Utility.rename_file(tmp_name,PathManager.get_url('tmp',self.next_download_file))
                
                #MOVE FILES TO LOCAL OR SCP
                local_dir = ds.local_directory_path
                if ds.download_to_local_dir:
                    root_dir = PathManager.get_url('root-dir')
                    if "{root-dir}" in local_dir:
                        local_dir = local_dir.replace("{root-dir}", root_dir)
                    Utility.copy_file(PathManager.get_url('tmp',self.next_download_file), local_dir)
                    Utility.remove_file(PathManager.get_url('tmp',self.next_download_file))
                
                #REPROJECT FROM 0-360 to -180-180
                old_path = "%s/%s" % (local_dir, self.next_download_file)
                Utility.reproject_netcdf(ds,old_path,old_path )

                #CREATE LATEST
                if ds.create_latest:
                    Utility.copy_file("%s/%s" % (local_dir, self.next_download_file),"%s/%s" % (local_dir, "latest.nc"))

                #CLEANUP IF NEEDED, try
                Utility.remove_file(tmp_name)
                
                #SET STAUS
                download_complete = True
            else:
                download_complete = False
        except Exception as e:
            print(e)
            is_error = True
        return download_complete, is_error

    def download_obdaac(self,ds):
        #CHECK VARS
        download_complete = False
        is_error = False

        try:
            #GET URL
            url = ds.data_download_url
            
            #REPLACE WITH FILE TO DOWNLOAD
            url = url.replace('{download_file_name}', self.next_download_file)

            #CHECK
            substrings_to_remove = [ds.download_file_prefix, ds.download_file_suffix]
            new_string = Utility.remove_substrings(self.next_download_file, substrings_to_remove)
            newstr = new_string
            infixstr = ds.download_file_infix
            if "_" in new_string:
                newsplot = new_string.split("_")
                infix_split = ds.download_file_infix.split('_')
                newstr =  newsplot[0]
                infixstr = infix_split[0]
            convert_to_datetime = datetime.strptime(newstr, infixstr)
            
            #CHECK FOR YEAR
            if "{year}" in url:
                url = url.replace('{year}', convert_to_datetime.strftime('%Y'))
            #CHECK FOR MONTH
            if "{month}" in url:
                url = url.replace('{month}', convert_to_datetime.strftime('%m'))
            
            #CHECK FOR DAY
            if "{day}" in url:
                url = url.replace('{day}', convert_to_datetime.strftime('%d'))

            print(url)
            
            #DOWNLOAD FILE
            result = Utility.download_obdaac(url,PathManager.get_url('tmp',self.next_download_file))            
            
            if os.path.exists("%s/%s" % (PathManager.get_url('tmp'),self.next_download_file)):
                #RENAME TO TMP IN THE SAME DIR
                tmp_name = "%s%s" % (PathManager.get_url('tmp',self.next_download_file), "_tmp.nc")
                Utility.rename_file(PathManager.get_url('tmp',self.next_download_file), tmp_name)

                #IF SUBSET OR VARIBLES
                if ds.has_variables or ds.subset:
                    print('subsetting')
                    output_file = "%s" % (PathManager.get_url('tmp',self.next_download_file))
                    is_subsetted = Utility.subset_netcdf(ds, tmp_name, output_file)
                    if not is_subsetted:
                        Utility.rename_file(tmp_name,PathManager.get_url('tmp',self.next_download_file))

                else:
                    Utility.rename_file(tmp_name,PathManager.get_url('tmp',self.next_download_file))
                
                #MOVE FILES TO LOCAL OR SCP
                local_dir = ds.local_directory_path
                if ds.download_to_local_dir:
                    root_dir = PathManager.get_url('root-dir')
                    if "{root-dir}" in local_dir:
                        local_dir = local_dir.replace("{root-dir}", root_dir)
                    Utility.copy_file(PathManager.get_url('tmp',self.next_download_file), local_dir)
                    Utility.remove_file(PathManager.get_url('tmp',self.next_download_file))
                
                #REPROJECT FROM 0-360 to -180-180
                old_path = "%s/%s" % (local_dir, self.next_download_file)
                Utility.reproject_netcdf(ds,old_path,old_path )
                
                #CREATE LATEST
                if ds.create_latest:
                    Utility.copy_file("%s/%s" % (local_dir, self.next_download_file),"%s/%s" % (local_dir, "latest.nc"))

                #CLEANUP IF NEEDED, try
                Utility.remove_file(tmp_name)

                download_complete = True
            else:
                download_complete = False
        except Exception as e:
            print(e)
            is_error = True
        return download_complete, is_error

    def download_copernicusmarine(self,ds):
        #CHECK VARS
        download_complete = False
        is_error = False
        try:
            #PREPARE PARAMETERS
            substrings_to_remove = [ds.download_file_prefix, ds.download_file_suffix]
            new_string = Utility.remove_substrings(self.next_download_file, substrings_to_remove)
            splitdates = new_string.split('_')
            infixsplit = ds.download_file_infix.split('_')

            #PARAMS TO BE PASSED
            start_datetime = datetime.strptime(splitdates[0], infixsplit[0])
            end_datetime = datetime.strptime(splitdates[1], infixsplit[1])
            dataset_id = ds.data_download_url
            varib = ds.variables
            variables = [x.strip() for x in varib.split(',')]
            new_file_name = self.next_download_file
            download_directory = ds.local_directory_path
            root_dir = PathManager.get_url('root-dir')

            #CHECK TO SEE IF THERE IS NEED TO CHANGE END DATE
            if ds.force_forecast:
                print('it is a 7-day forecast')
                end_datetime = Utility.add_time(end_datetime,0,ds.force_days, 0,0)
            
            if "{root-dir}" in download_directory:
                download_directory = download_directory.replace("{root-dir}", root_dir)

            #DOWNLOAD THE DATA
            get_data = Utility.download_from_copernicus(ds,dataset_id, variables, start_datetime, end_datetime,\
                new_file_name,download_directory)
            
            if get_data:
                #REPROJECT FROM 0-360 to -180-180
                old_path = "%s/%s" % (download_directory, new_file_name)
                Utility.reproject_netcdf(ds,old_path,old_path )
                #CREATE LATEST
                if ds.create_latest:
                    Utility.copy_file("%s/%s" % (download_directory, new_file_name),"%s/%s" % (download_directory, "latest.nc"))
                download_complete = True
            else:
                download_complete = False
            
        except Exception as e:
            is_error = True
            print(e)
        return download_complete, is_error

    def dataDownload(self):
        #GET DATASET
        url= PathManager.get_url('ocean-api','dataset')
        #dataset_url = "https://dev-oceanportal.spc.int/v1/api/dataset/%s" % (self.dataset_id)
        dataset_url = "%s/%s" % (url,self.dataset_id)
        print(dataset_url)
        ds = initialize_datasetController(dataset_url)

        #CHECK IF FILE EXISTS AND DOWNLOAD
        download_succeed, is_error = False, False

        #create product directory if it does not exist
        self.create_product_directory(ds)

        #SET TO RUNNING
        Utility.update_api(PathManager.get_url('ocean-api','task_download',str(self.id)+"/"), {"health":"Running"})
        
        if ds.download_method == 1:
            print('download with https')
            download_succeed, is_error = self.download_http(ds)
        elif ds.download_method == 2:
            print('downloading with obdaac..')
            download_succeed, is_error = self.download_obdaac(ds)
        elif ds.download_method == 3:
            print('downloading with copernicusmarine..')
            download_succeed, is_error = self.download_copernicusmarine(ds)
        else:
            print('nothing to download.')
        
        #COMPULSORY THINGS TO DO, UPDATE THE API
        new_file_name,new_download_time = self.generate_next_download_filename(ds)
        print(new_file_name,new_download_time)
        #Utility.update_tasks(download_succeed, is_error, new_file_name,new_download_time,self,ds)
        
        print('data download completed.')

#LOAD VARIABLES FROM API INTO THE CLASS
def initialize_taskController(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        enqueue = []
        for item in data:
            queue = taskController(item['id'],item['task_name'].strip(), item['class_id'].strip(), item['dataset_id'],item['status'].strip(),\
                                item['priority'].strip(),\
                                    item['duration'].strip(),item['task_start_time'],item['next_run_time'],\
                                        item['last_run_time'],item['next_download_file'].strip(),item['last_download_file'].strip(),\
                                        item['enabled'],item['health'].strip(),item['fail_count'],item['success_count'],item['reset_count'],\
                                            item['attempt_count'],item['predecessor_class'],item['predecessor_class_id'],item['successor_class'],\
                                            item['successor_class_id'],\
                                                item['created_by'].strip(),item['launched_by'].strip(),item['retain'],item['retention_days'])
            enqueue.append(queue)
        return enqueue
    else:
        print("Failed to retrieve data: {response.status_code}")
        return None