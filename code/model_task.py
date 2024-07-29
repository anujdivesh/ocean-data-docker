
class task:
    def __init__(self, id, task_name, class_id, dataset_id,status,priority,\
                 duration,task_start_time,next_run_time,last_run_time,next_download_file,last_download_file,enabled,health,fail_count,\
                    success_count,reset_count,attempt_count,predecessor_class,predecessor_class_id,successor_class,successor_class_id,created_by,launched_by,\
                        retain,retention_days):
        self.id = id
        self.task_name = task_name
        self.class_id = class_id
        self.dataset_id = dataset_id
        self.status = status
        self.priority = priority
        self.duration = duration
        self.task_start_time = task_start_time
        self.next_run_time = next_run_time
        self.last_run_time = last_run_time
        self.next_download_file = next_download_file
        self.last_download_file = last_download_file
        self.enabled = enabled
        self.health = health
        self.fail_count = fail_count
        self.success_count = success_count
        self.reset_count = reset_count
        self.attempt_count = attempt_count
        self.predecessor_class = predecessor_class
        self.predecessor_class_id = predecessor_class_id
        self.successor_class = successor_class
        self.successor_class_id = successor_class_id
        self.created_by = created_by
        self.launched_by = launched_by
        self.retain = retain
        self.retention_days = retention_days