from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from typing import Optional

class DataChunk(BaseModel):

    _id: Optional[ObjectId]
    chunk_text: str = Field(min_length=1)
    chunk_metadata: dict
    chunk_order: int = Field(gt=0)
    chunk_project_id: ObjectId # the link between project and chunk

    class Config:
        arbitrary_types_allowed = True