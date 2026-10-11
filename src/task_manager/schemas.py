from typing import Literal

from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    title: str=Field(min_length=3,max_length=50)
    priority: Literal["low", "medium", "high"]
    description: str="No description"
    
    @field_validator("title")
    @classmethod
    def title_uppercase(cls,value):
        if not value[0].isupper():
            raise ValueError("The title must starts with an uppercase letter")
        return value 
    
class TaskUpdate(BaseModel):
    title: str|None=Field(min_length=3,max_length=50)
    priority: Literal["low", "medium", "high"] | None=None
    description: str|None =None
    
    @field_validator("title")
    @classmethod
    def title_uppercase(cls,value):
        if value is not None:
            if not value[0].isupper():
                raise ValueError("The title must starts with an uppercase letter")
            return value     
    

class TaskResponse(BaseModel):
    task_id:int
    title: str
    priority: str
    description: str
    status: str  
    

if __name__ == "__main__": 
    task_test=TaskCreate(title="Read Book",priority="medium",description="read book before sleep at 9 pm") 
    print(task_test.model_dump())
    print(task_test.model_dump_json())   
  
  
  