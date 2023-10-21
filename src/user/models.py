from pydantic import BaseModel, Field
from utils import id
from typing import List

class User(BaseModel):
   id: str
   username: str
   total_likes: int = Field(default=0)
   comics_id: List[str] = Field(default=[])
   
class CreateUserDTO(BaseModel):
   username: str