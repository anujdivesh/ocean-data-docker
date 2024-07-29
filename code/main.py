from controller_task import initialize_taskController
from datetime import datetime
from utility_functions import Utility
from controller_server_path import PathManager

if __name__ == "__main__":
    url= PathManager.get_url('ocean-api','tasks')
    tasks = initialize_taskController(url)
    
    for task in tasks:
        if task.class_id == "download":
            execute = Utility.time_diff(datetime.now(),datetime.strptime(task.next_run_time,"%Y-%m-%dT%H:%M:%S.000Z"))
            #REMOVE THIS IN PROD
            execute = True
            if execute and task.enabled:
                print('Executing Task No.%s - %s' % (task.id, task.task_name))
                task.dataDownload()