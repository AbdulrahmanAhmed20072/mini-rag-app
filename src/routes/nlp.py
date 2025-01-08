from fastapi import FastAPI, APIRouter, status, Request
from fastapi.responses import JSONResponse
from routes.schemes import PushRequest, SearchRequest
from models import ProjectModel, ChunkModel
from controllers import NLPController
from models.enums import ResponseSignal
import logging

logging.getLogger("uvicorn.error")

nlp_router = APIRouter(
    prefix="/api/v1/nlp",
    tags = ["api_v2", "nlp"]
)

@nlp_router.post("/index/push/{project_id}")
async def index_project(request: Request, project_id: str, push_request: PushRequest):
    
    project_model = await ProjectModel.create_instance(
        db_client = request.app.db_client
    )
    
    chunk_model = await ChunkModel.create_instance(
        db_client = request.app.db_client
        )
    
    project = await project_model.get_project_or_create_one(project_id = project_id)

    if not project:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                "signal" : ResponseSignal.PROJECT_NOT_FOUND_ERROR.value
            }
        )
    
    nlp_controller = NLPController(
        vectordb_client = request.app.vectordb_client,
        generation_client = request.app.generation_client,
        embedding_client = request.app.embedding_client,
        template_parser = request.app.template_parser
        )
    
    page_no = 1
    has_records = True
    inserted_items_count = 0

    while has_records:

        page_chunks = await chunk_model.get_project_chunks(
            project_id = project.id, page_no = page_no)
        
        if not page_chunks or len(page_chunks) == 0:
            has_records = False
            break
        
        page_no += 1

        is_inserted = nlp_controller.index_into_vector_db(
            project = project,
            chunks = page_chunks,
            do_reset = push_request.do_reset,
        )

        if not is_inserted:
            return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                "signal" : ResponseSignal.INSERT_INTO_VECTORDB_ERROR.value
            }
        )

        inserted_items_count += len(page_chunks)

    return JSONResponse(
            content = {
                "signal" : ResponseSignal.INSERT_INTO_VECTORDB_SUCCESS.value,
                "inserted_items_count" : inserted_items_count
            }
        )

@nlp_router.get("/index/info/{project_id}")
async def get_project_index_info(request: Request, project_id: str):
    
    project_model = await ProjectModel.create_instance(
        db_client = request.app.db_client)

    project = await project_model.get_project_or_create_one(project_id = project_id)

    nlp_controller = NLPController(
        vectordb_client = request.app.vectordb_client,
        generation_client = request.app.generation_client,
        embedding_client = request.app.embedding_client,
        template_parser = request.app.template_parser
        )
    
    collection_info = nlp_controller.get_vector_db_collection_info(project)

    if not collection_info:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                "signal" : ResponseSignal.VECTORDB_COLLECTION_NOT_FOUND.value,
            }
        )

    return JSONResponse(
            content = {
                "signal" : ResponseSignal.VECTORDB_COLLECTION_RETRIEVED.value,
                "collection_info" : collection_info,
            }
        )

@nlp_router.post("/index/search/{project_id}")
async def nlp_index_search(request: Request, project_id: str, search_request: SearchRequest):

    project_model = await ProjectModel.create_instance(
        db_client = request.app.db_client)

    project = await project_model.get_project_or_create_one(project_id = project_id)


    nlp_controller = NLPController(
        vectordb_client = request.app.vectordb_client,
        generation_client = request.app.generation_client,
        embedding_client = request.app.embedding_client,
        template_parser = request.app.template_parser
        )

    results = nlp_controller.search_vector_db_collection(
        project = project,
        text = search_request.text,
        limit = search_request.limit
    )

    if not results:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                "signal" : ResponseSignal.VECTORDB_SEARCH_ERROR.value,
            }
        )

    return JSONResponse(
            content = {
                "signal" : ResponseSignal.VECTORDB_SEARCH_SUCCESS.value,
                "collection_info" : [res.dict() for res in results],
            }
        )

@nlp_router.post("/index/answer/{project_id}")
async def answer_rag(request: Request, project_id: str, search_request: SearchRequest):

    project_model = await ProjectModel.create_instance(
        db_client = request.app.db_client)

    project = await project_model.get_project_or_create_one(project_id = project_id)


    nlp_controller = NLPController(
        vectordb_client = request.app.vectordb_client,
        generation_client = request.app.generation_client,
        embedding_client = request.app.embedding_client,
        template_parser = request.app.template_parser
        )
    
    answer, full_prompt, chat_history = nlp_controller.answer_rag_question(
        project = project, query = search_request.text, limit = search_request.limit)
    
    if not answer:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                "signal" : ResponseSignal.RAG_ANSWER_ERROR.value,
            }
        )

    return JSONResponse(
            content = {
                "signal" : ResponseSignal.RAG_ANSWER_SUCCESS.value,
                "answer" : answer,
                "full_prompt" : full_prompt,
                "chat_history" : chat_history
            }
        )

# [{'role': <CohereEnums.SYSTEM: 'system'>, 
#   'content': "You are an assistant to generate a response for the user.\nYou will be provided by a set of documents associated with the user's query.\nYou have to generate a response based on the documents provided."},
# {'role': 'user', 'content': '## Document No: 1\n### Content: Society called him Handsome Signoles. His name was Viscount Gontran-Joseph de Signoles.\n\nBased only on the above documents, please generate an answer for the user.\n## Answer:'}]