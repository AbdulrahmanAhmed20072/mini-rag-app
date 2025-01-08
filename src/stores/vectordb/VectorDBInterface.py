from abc import ABC, abstractmethod
from typing import List
from models.db_schemes import RetrievedDocument

class VectorDBInterface(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def is_collection_exists(self, collection_name) ->bool:
        pass

    @abstractmethod
    def list_all_collections(self) -> List:
        pass

    @abstractmethod
    def get_collection_info(self, collection_name) -> dict:
        pass

    @abstractmethod
    def delete_collection(self, collection_name):
        pass

    @abstractmethod
    def create_collection(self, collection_name: str , 
                          embedding_size: int ,
                          do_reset: bool = False):
        pass

    @abstractmethod
    def insert_one(self, collection_name: str, text: str, vector: list,
                   metadata: dict, record_id: str):
        pass

    @abstractmethod
    def insert_many(self, collection_name: str, texts: List[str],
                     vectors: List[list], metadatas: List[dict],
                    record_ids: List[str], batch_size: int = 50):
        pass

    @abstractmethod
    def search_by_vector(self, collection_name: str, vector: list, limit: int) -> List[RetrievedDocument]:
        pass