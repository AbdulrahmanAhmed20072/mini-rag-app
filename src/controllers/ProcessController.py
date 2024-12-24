from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from models.enums import ProcessingEnums
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ProcessController( BaseController ):

    def __init__(self, project_id: str):

        super().__init__()

        self.project_id = project_id
        self.project_path = ProjectController().get_project_path( project_id = self.project_id )
    
    def get_file_extension(self, file_id: str):

        return os.path.splitext(file_id)[-1]

    def get_file_loader(self, file_id: str):
        
        file_extension = self.get_file_extension(file_id)

        file_path = os.path.join(self.project_path, file_id)

        if file_extension == ProcessingEnums.TXT.value:
            return TextLoader(file_path, encoding = "utf-8")

        elif file_extension == ProcessingEnums.PDF.value:
            return PyMuPDFLoader(file_path)
        
        return None
    
    def get_file_content(self, file_id: str):

        loader = self.get_file_loader(file_id)

        return loader.load()
    
    def process_file_content(self, file_content: list, chunk_size: int, chunk_overlap: int):

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,
            length_function = len
        )

        file_content_texts = [i.page_content for i in file_content]
        file_content_meta = [i.metadata for i in file_content]

        chunks = text_splitter.create_documents(file_content_texts, metadatas = file_content_meta)

        return chunks