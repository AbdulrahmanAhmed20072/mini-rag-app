from pydantic import BaseModel
from bson.objectid import ObjectId
from typing import Optional

class project(BaseModel):

    _id: Optional(ObjectId)