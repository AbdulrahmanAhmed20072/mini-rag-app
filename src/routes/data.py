from fastapi import FastAPI, APIRouter, UploadFile, Depends, status # type: ignore
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController # made by __init__.py file
import aiofiles
import os
from models import ResponseSignal

data_router = APIRouter(
    prefix = "/api/v1/data",
    tags = ["api_v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data( project_id: str , file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):
    
    is_valid, result_signal = DataController().validate_uploaded_file( file = file )

    if not is_valid:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {"result_signal" : result_signal}
        )
    
    project_dir_path = ProjectController().get_project_path(project_id = project_id)
    file_path = os.path.join(project_dir_path, file.filename)

    #open the uploaded file and load it in the dist using aiofile by the chunk size
    async with aiofiles.open(file_path , "wb") as f:
        while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
            await f.write(chunk)
    
    return JSONResponse(
            content = {"result_signal" : ResponseSignal.FILE_UPLOAD_SUCCESS.value}
        )