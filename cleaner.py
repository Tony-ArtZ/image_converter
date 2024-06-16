import os
import time
from converter import delete_task
from converter import tasks

def cleanup_old_files():
    current_time = time.time()
    for task_id, task_info in list(tasks.items()):
        if task_info["status"] == "completed":
            if current_time - task_info["created_at"] > 1800: 
                file_path = task_info["output_path"]
                if os.path.exists(file_path):
                    os.remove(file_path)
                    delete_task(task_id)