from qdrant_client import QdrantClient, models
from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import DistanceMethodEnums
import logging
from typing import List

class QdrantDBProvider(VectorDBInterface):

    def __init__(self, db_path: str, distance_method: str):
        
        self.client = None
        self.db_path = db_path

        if distance_method == DistanceMethodEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodEnums.DOT.value:
            self.distance_method = models.Distance.DOT
        
        self.logger = logging.getLogger(__name__)

    def connect(self):
        self.client = QdrantClient(path = self.db_path)
    
    def disconnect(self):
        return None
    
    def is_collection_exists(self, collection_name) ->bool:

        return self.client.collection_exists(collection_name = collection_name)
    
    def list_all_collections(self) -> List:
        
        return self.client.get_collections()
    
    def get_collection_info(self, collection_name) -> dict:

        return self.client.get_collection(collection_name = collection_name)
    
    def delete_collection(self, collection_name):

        if self.is_collection_exists(collection_name) is True:
            return self.client.delete_collection(collection_name = collection_name)
        else:
            return None

    def create_collection(self, collection_name: str , 
                          embedding_size: int ,
                          do_reset: bool = False):
        if do_reset:
            _ = self.delete_collection(collection_name = collection_name)

        if not self.is_collection_exists(collection_name = collection_name):
            _ = self.client.create_collection(
                collection_name = collection_name,
                vectors_config = models.VectorParams(
                    size = embedding_size,
                    distance = self.distance_method
                )
            )

            return True
        
        return False
    
    def insert_one(self, collection_name: str, text: str, vector: list,
                   metadata: dict, record_id: str):
        
        if not self.is_collection_exists(collection_name = collection_name):
            self.logger.error(f"can not insert record to non-existed collection {collection_name}")
            return False
        
        try:
            _ = self.client.upload_records(
                collection_name = collection_name,
                records = [
                    models.Record(
                        vector = vector,
                        payload = {
                            "text" : text, "metadata" : metadata
                        }
                    )
                ]
            )
        except Exception as e:
                self.logger.error(f"error while inserting batch: {e}")
                return False
            
        return True

    def insert_many(self, collection_name: str, texts: List[str],
                    vectors: List[list], metadatas: List[dict],
                    record_ids: List[str], batch_size: int = 50):
        
        # if metadatas was None convert it to list of None so we can iterate
        metadatas = [None] * len(metadatas) if not metadatas else metadatas
        # if record_ids was None convert it to list of None so we can iterate
        record_ids = [None] * len(record_ids) if not record_ids else record_ids

        for i in range(0, len(vectors), batch_size):

            batch_texts = texts[i : i + batch_size]
            batch_vectors = vectors[i : i + batch_size]
            batch_metadatas = metadatas[i : i + batch_size]

            batch_record = [

                models.Record(
                    vector = batch_vectors[i],
                    payload = {
                        "text" : batch_texts[i], "metadata" : batch_metadatas[i]
                    }
                )

                for i in range(len(batch_texts))
            ]

            try :

                _ = self.client.upload_records(
                        collection_name = collection_name,
                        records = [batch_record]
                        )
            
            except Exception as e:
                self.logger.error(f"error while inserting batch: {e}")
                return False
            
        return True
    
    def search_by_vector(self, collection_name: str, vector: list, limit: int = 5):
        
        return self.client.search(
            collection_name = collection_name,
            vector = vector,
            limit = limit
        )