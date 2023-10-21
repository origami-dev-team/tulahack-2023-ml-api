from pydantic import BaseModel, Field

class Comics(BaseModel):
    id: str
    title: str
    author: str
    url: str
    preview: str
    likes: int = Field(default=0)
