from controller_task import initialize_taskController
from datetime import datetime
from utility_functions import Utility
from controller_server_path import PathManager
from update_thredds import thredds


if __name__ == "__main__":
    url= PathManager.get_url('ocean-api','task_download')
    tasks = initialize_taskController(url)
    
    for task in tasks:
        if task.class_id == "download":
            execute = Utility.time_diff(datetime.now(),datetime.strptime(task.next_run_time,"%Y-%m-%dT%H:%M:%SZ"))
            #REMOVE THIS IN PROD
            #execute = True
            if task.id == 3:
                print('Executing Task No.%s - %s' % (task.id, task.task_name))
                #task.dataDownload()
    
    #Updating DateRange from Thredds
    api_url = PathManager.get_url('ocean-api',"layer_web_map/")
    api_response = thredds.get_data_from_api(api_url)

    for x in api_response:
        if x['update_thredds']:
            url = x['url']
            period = x['period']

            #CHECK EACH
            if period == 'COMMA':
                thredds.get_specific(x)
            elif period == 'PT6H' or period == "P1D":
                thredds.get_6hourly(x)
            elif period == 'OPENDAP':
                thredds.get_specific_stamp(x)
