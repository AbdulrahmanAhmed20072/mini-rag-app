from fastapi import FastAPI, APIRouter, UploadFile, Depends, status, Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController, BaseController
import aiofiles
import os
from models import ResponseSignal
import logging
from routes.schemes import ProcessRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schemes.data_chunk import DataChunk
from models.enums import ResponseEnums
# from bson.objectid import ObjectId

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix = "/api/v1/data",
    tags = ["api_v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data( request: Request, project_id: str , file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):
    
    project_model = ProjectModel( db_client = request.app.db_client )

    project = await project_model.get_project_or_create_one(project_id)

    Data_Controller = DataController()

    is_valid, result_signal = Data_Controller.validate_uploaded_file( file = file )

    if not is_valid:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {"result_signal" : result_signal}
        )
    
    # project_dir_path = ProjectController().get_project_path(project_id = project_id)

    file_path, file_id = Data_Controller.generate_unique_filepath(
        orig_file_name = file.filename , project_id = project_id)

    try:
        #open the uploaded file and load it in the dist using aiofile by the chunk size
        async with aiofiles.open(file_path , "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger(f"error while uploading file: {e}")

        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {"result_signal" : ResponseSignal.FILE_UPLOAD_FAILED.value}
        )

    return JSONResponse(
            content = {"result_signal" : ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                       "file_id" : file_id, 
                       "project_id": str(project.id),
                       }
        )

@data_router.post("/process/{project_id}")
async def process_endpoint(request: Request, project_id: str, process_request: ProcessRequest):
    
    project_model = ProjectModel( db_client = request.app.db_client )

    project = await project_model.get_project_or_create_one(project_id)

    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    chunk_overlap = process_request.overlap_size
    chunk_reset = process_request.do_reset

    chunk_model = ChunkModel(db_client = request.app.db_client)

    if chunk_reset == 1:
        _ = await chunk_model.delete_chunks_by_project_id(project.id)

    # check if the passed file is existed at project_id dir, i made it (^-^)
    if not os.path.exists(os.path.join(BaseController().files_dir, f"{project_id}/{file_id}")):
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {"result_signal" : ResponseSignal.FILE_PROCESS_NOT_FOUND.value}
        )

    process_controller = ProcessController(project_id)

    file_content = process_controller.get_file_content(file_id)

    file_chunks = process_controller.process_file_content(
        file_content = file_content, chunk_size = chunk_size, chunk_overlap = chunk_overlap)
    
    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {"result_signal" : ResponseSignal.FILE_PROCESS_FAILED.value}
        )
    
    file_chunks_records = [

        DataChunk(
            chunk_text = chunk.page_content,
            chunk_metadata = chunk.metadata,
            chunk_order = i+1,
            chunk_project_id = project.id,
        )

        for i, chunk in enumerate(file_chunks)
    ]

    no_records = await chunk_model.insert_many_chunks(chunks = file_chunks_records)

    return no_records