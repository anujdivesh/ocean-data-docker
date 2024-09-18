
class dataset:
    def __init__(self, id, short_name, long_name, data_type,data_provider,data_source_url,data_download_url,login_credentials_required,username,\
                 password,API_key,download_method,download_file_prefix,download_file_infix,download_file_suffix,download_file_type,\
                    download_to_local_dir,local_directory_path,scp,scp_server_path,frequency_minutes,frequency_hours,frequency_days,frequency_months,\
                        check_minutes,check_hours,check_days,check_months,has_variables,variables,subset,convert_longitude,xmin_xmax,ymin_ymax,create_latest,\
                        force_forecast, force_days):
        self.id = id
        self.short_name = short_name
        self.long_name = long_name
        self.data_type = data_type
        self.data_provider = data_provider
        self.data_source_url = data_source_url
        self.data_download_url = data_download_url
        self.login_credentials_required = login_credentials_required
        self.username = username
        self.password = password
        self.API_key = API_key
        self.download_method = download_method
        self.download_file_prefix = download_file_prefix
        self.download_file_infix = download_file_infix
        self.download_file_suffix = download_file_suffix
        self.download_file_type = download_file_type
        self.download_to_local_dir = download_to_local_dir
        self.local_directory_path = local_directory_path
        self.scp = scp
        self.scp_server_path = scp_server_path
        self.frequency_minutes = frequency_minutes
        self.frequency_hours = frequency_hours
        self.frequency_days = frequency_days
        self.frequency_months = frequency_months
        self.check_minutes = check_minutes
        self.check_hours = check_hours
        self.check_days = check_days
        self.check_months = check_months
        self.has_variables = has_variables
        self.variables = variables
        self.subset = subset
        self.convert_longitude = convert_longitude
        self.xmin_xmax = xmin_xmax
        self.ymin_ymax = ymin_ymax
        self.create_latest = create_latest
        self.force_forecast = force_forecast
        self.force_days = force_days