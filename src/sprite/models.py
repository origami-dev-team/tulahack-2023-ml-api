from pydantic import BaseModel, Field
from datetime import datetime
from utils import now
from constants import SpriteCategory


class Sprite(BaseModel):
    id: str
    category: SpriteCategory
    url: str
    created_at: datetime = Field(default_factory=now)
    
class GenerateSpriteDTO(BaseModel):
    prompt: str
    
