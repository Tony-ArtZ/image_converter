from fastapi import FastAPI, File, UploadFile, HTTPException, Form, BackgroundTasks
from fastapi.responses import FileResponse
import constants
import uuid
import os
from typing import Dict
from converter import get_task_status, convert_image
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from cleaner import cleanup_old_files
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import uvicorn

scheduler = AsyncIOScheduler()
scheduler.add_job(cleanup_old_files, IntervalTrigger(minutes=30))

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, replace with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")


@app.get("/formats")
def get_formats():
    return {"formats": constants.SUPPORTED_FORMATS}

@app.post("/upload/")
async def upload_image(background_tasks: BackgroundTasks, file: UploadFile = File(...), output_format: str = Form(...)):
    if not file:
        raise HTTPException(status_code=400, detail="File is required")
    
    if output_format.upper() not in constants.SUPPORTED_FORMATS:
        raise HTTPException(status_code=400, detail="Unsupported format")
    
    # Generate a unique filename
    task_id = str(uuid.uuid4())
    filename = f"{task_id}.{output_format.lower()}"
    input_path = os.path.join(constants.UPLOAD_DIR, f"input_{filename}")
    output_path = os.path.join(constants.CONVERTED_DIR, filename)
    
    # Save the uploaded file
    with open(input_path, "wb") as buffer:
        buffer.write(await file.read())
        
    # Schedule conversion    
    background_tasks.add_task(convert_image, task_id, input_path, output_path, output_format)
    
    return {"task_id": task_id, "message": "Conversion started"}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    return get_task_status(task_id)

@app.get("/download/{filename}")
async def download_image(filename: str):
    file_path = os.path.join(constants.CONVERTED_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    raise HTTPException(status_code=404, detail="File not found")

@app.on_event("startup")
async def startup_event():
    scheduler.start()
    os.makedirs(constants.UPLOAD_DIR, exist_ok=True)
    os.makedirs(constants.CONVERTED_DIR, exist_ok=True)
    
async def shutdown_event():
    scheduler.shutdown()
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=os.getenv("PORT", default=5000), log_level="info")