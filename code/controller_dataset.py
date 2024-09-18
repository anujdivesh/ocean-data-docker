from model_dataset import dataset
import requests
from controller_country import initialize_countryController

class datasetController(dataset):
    def __init__(self, id, short_name, long_name, type,data_provider,data_source_url,data_download_url,login_credentials_required,username,\
                 password,API_key,download_method,download_file_prefix,download_file_infix,download_file_suffix,download_file_type,\
                    download_to_local_dir,local_directory_path,scp,scp_server_path,frequency_minutes,frequency_hours,frequency_days,frequency_months,\
                        check_minutes,check_hours,check_days,check_months,has_variables,variables,subset,convert_longitude,xmin_xmax,ymin_ymax,create_latest,\
                        force_forecast, force_days):
        super().__init__(id, short_name, long_name, type,data_provider,data_source_url,data_download_url,login_credentials_required,username,\
                 password,API_key,download_method,download_file_prefix,download_file_infix,download_file_suffix,download_file_type,\
                    download_to_local_dir,local_directory_path,scp,scp_server_path,frequency_minutes,frequency_hours,frequency_days,frequency_months,\
                        check_minutes,check_hours,check_days,check_months,has_variables,variables,subset,convert_longitude,xmin_xmax,ymin_ymax,create_latest,\
                        force_forecast, force_days)

    def dataDownload(self):
        #CHECK WHEATHER TO SUBSET THE DATASET
        subset_region = []
        if self.subset == True:
            url = "https://dev-oceanportal.spc.int/v1/api/country/%s" % (self.subset_region)
            subset_region.append(initialize_countryController(url))

        
        if self.download_method == "ncss":
            print('downloading with thredds..')

        elif self.download_method == "http":
            print('downloading with http..')
        elif self.download_method == "ncss":
            print('downloading with corpernicus..')
        else:
            print('nothing to download.')
            

def initialize_datasetController(url):
    response = requests.get(url)
    if response.status_code == 200:
        item = response.json()
        dataset = datasetController(item['id'],item['short_name'].strip(), item['long_name'].strip(),item['data_type'], item['data_provider'].strip(),item['data_source_url'].strip(),\
                                item['data_download_url'].strip(),item['login_credentials_required'],item['username'],item['password'],\
                                item['API_key'],item['download_method'],item['download_file_prefix'].strip(),item['download_file_infix'].strip(),\
                                    item['download_file_suffix'].strip(),item['download_file_type'].strip(),item['download_to_local_dir'],\
                                        item['local_directory_path'].strip(),item['scp'],item['scp_server_path'],item['frequency_minutes'],\
                                            item['frequency_hours'],item['frequency_days'],item['frequency_months'],item['check_minutes'],\
                                                item['check_hours'],item['check_days'],item['check_months'],item['has_variables'],str(item['variables']).strip(),\
                                            item['subset'],item['convert_longitude'],str(item['xmin_xmax']).strip(),str(item['ymin_ymax']).strip(),item['create_latest'], \
                                            item['force_forecast'],item['force_days'])
        return dataset
    else:
        print("Failed to retrieve data: {response.status_code}")
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