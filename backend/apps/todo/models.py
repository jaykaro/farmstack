import uuid
from typing import Optional
from pydantic import BaseModel, Field


# This is for creating a new task
class TaskModel(BaseModel):
    # whenever mongodb assigns an id, it will assign a type object id  
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    completed: bool = False

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example":{
                "id": "1234567",
                "name": "My Important Task",
                "completed":False
            }
        }


# This is for when we are updating a new task
class UpdateTaskModel(BaseModel):
    name: Optional(str)
    completed: Optional(bool)


    class Config:
        schema_extra = {
            "example":{
                "name":"My other important task",
                "completed":True
            }
        }

