from pydantic import BaseModel, Field, field_validator
from bson.objectid import ObjectId
from typing import Optional

class project(BaseModel):

    _id: Optional[ObjectId]
    project_id: str = Field(min_length = 1)

    @field_validator("project_id")
    def validate_projext_id(cls, value):

        if not value.isalnum():
            raise ValueError("project_id must be alphanumeric")
        
        return value
 
    class Config:
        arbitary_types_allowed = True