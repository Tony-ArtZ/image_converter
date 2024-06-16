from PIL import Image
import asyncio
import os
from typing import Dict
import time
from datetime import datetime

tasks: Dict[str, Dict] = {}

async def convert_image(task_id: str, input_path: str, output_path: str, output_format: str):
    try:
        tasks[task_id] = {"status": "processing"}
        
        def _convert():
            with Image.open(input_path) as img:
                if output_format == "JPEG":
                    img = img.convert("RGB")
                img.save(output_path, output_format)

        await asyncio.to_thread(_convert)
        tasks[task_id] = {
            "status": "completed",
            "created_at": time.time(),
            "output_path": output_path
        }
    except Exception as e:
        tasks[task_id] = {"status": "failed", "error": str(e)}
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)

            
def get_task_status(task_id: str):
    return tasks.get(task_id, {"status": "not_found"})

def delete_task(task_id:str):
    if task_id in tasks:
        del tasks[task_id]
        return {"message": "Task deleted"}
    return {"message": "Task not found"}