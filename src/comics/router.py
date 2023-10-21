from fastapi import APIRouter, UploadFile, Form
from database import firestore
from typing import Annotated, List
from .models import Comics
from utils import id
from constants import Collection

router = APIRouter()

@router.get("/")
async def get_all() -> List[Comics]:
    all = await firestore.get_all(collection=Collection.Comics)
    return [Comics(**one) for one in all]

@router.post("/")
async def upload(title: Annotated[str, Form()], author: Annotated[str, Form()], file: UploadFile) -> Comics:
    file_id = id()
    url = await firestore.upload_file(file=file, folder=Collection.Comics, id=file_id)
    comics = Comics(id=file_id, title=title, author=author, url=url) 
    sprite = await firestore.create(collection=Collection.Comics, data=comics.model_dump())
    return Comics(**sprite)

    
