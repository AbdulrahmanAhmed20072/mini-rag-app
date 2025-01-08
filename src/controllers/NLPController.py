from .BaseController import BaseController
from models.db_schemes import Project, DataChunk
from stores.llm.LLMEnums import DocumentTypeEnum
from helpers.config import get_settings
from typing import List
import json

class NLPController(BaseController):

    def __init__(self, vectordb_client, generation_client,
                       embedding_client, template_parser):
        super().__init__()

        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client
        self.template_parser = template_parser

    def create_project_name(self,project_id: str):

        return f"collection_{project_id}".strip()
    
    def reset_vector_db_collection(self, project: Project):

        collection_name = self.create_project_name(project_id = project.project_id)
        return self.vectordb_client.delete_collection(collection_name = collection_name)
    
    def get_vector_db_collection_info(self, project: Project):

        collection_name = self.create_project_name(project_id = project.project_id)
        collection_info = self.vectordb_client.get_collection_info(collection_name)

        return json.loads(
            json.dumps(collection_info, default= lambda x: x.__dict__)
            )
    
    def index_into_vector_db(self, project: Project, chunks: List[DataChunk],
                                   do_reset: bool = False):
        
        # step 1: get collection name
        collection_name = self.create_project_name(project_id = project.project_id)

        # step 2: manage chunks
        texts = [chunk.chunk_text for chunk in chunks]
        metadatas = [chunk.chunk_metadata for chunk in chunks]

        idx = 0
        chunk_ids = list(range(idx, idx + len(chunks)))
        idx += len(chunks)

        vectors = [
            
            self.embedding_client.embed_text(
                text = text, document_type = DocumentTypeEnum.DOCUMENT.value
            )

            for text in texts
        ]

        # step 3: create collection
        _ = self.vectordb_client.create_collection(
            collection_name = collection_name,
            embedding_size = self.embedding_client.embedding_size,
            do_reset = do_reset
        )

        # step 4: insert into vector db
        is_inserted = self.vectordb_client.insert_many(
            collection_name = collection_name,
            texts = texts,
            vectors = vectors,
            metadatas = metadatas,
            record_ids = chunk_ids
            )
        
        return is_inserted
    
    def search_vector_db_collection(self, project: Project, text: str, limit: int = 5):

        # step 1: get collection name
        collection_name = self.create_project_name(project_id = project.project_id)

        # step 2: get text embedding vector
        embed_vector = self.embedding_client.embed_text(
            text = text,
            document_type = DocumentTypeEnum.QUERY.value
        )

        if not embed_vector or len(embed_vector) == 0:
            return False

        # step 3: do semantic search
        results = self.vectordb_client.search_by_vector(
            collection_name = collection_name,
            vector = embed_vector,
            limit = limit
        )

        if not results:
            return False
        
        return results
    
    def answer_rag_question(self, project: Project, query: str, limit: int = 5):

        answer, full_prompt, chat_history = None, None, None

         # step 1: retrieve related documents
        retrieved_documents = self.search_vector_db_collection(
            project = project, text = query, limit = limit
        )

        if not retrieved_documents or len(retrieved_documents) == 0:
            return answer, full_prompt, chat_history
        
        # step 2: construct LLM prompts
        system_prompt = self.template_parser.get("rag", "system_prompt")

        documents_prompts = "\n".join([

            self.template_parser.get("rag", "document_prompt", {
                "doc_num" : i + 1,
                "chunk_text" : doc.text
            })

            for i, doc in enumerate(retrieved_documents)
        ])

        footer_prompt = self.template_parser.get("rag", "footer_prompt")

        chat_history = [
            self.generation_client.construct_prompt(
                prompt = system_prompt,
                role = self.generation_client.enums.SYSTEM
            )
        ]

        full_prompt = "\n\n".join([documents_prompts, footer_prompt])

        answer = self.generation_client.generate_text(
            prompt = full_prompt, chat_history = chat_history
        )
        
        print("chat history is: ",chat_history)
            
        return answer, full_prompt, chat_history