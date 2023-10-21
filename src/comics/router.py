from random import randint
from fastapi import APIRouter, UploadFile, Form
from database import firestore
from typing import Annotated, List
from .models import Comics
from sprite.models import Sprite
from utils import id
from constants import Collection, SpriteCategory

router = APIRouter()

@router.get("")
async def get_all() -> List[Comics]:
    all = await firestore.get_all(collection=Collection.Comics)
    return [Comics(**one) for one in all]

@router.post("")
async def upload(title: Annotated[str, Form()], author: Annotated[str, Form()], file: UploadFile) -> Comics:
    file_id = id()
    url = await firestore.upload_file(file=file, folder=Collection.Comics, id=file_id)
    all = await firestore.get_all(collection=Collection.Sprite)
    sprites = [Sprite(**one) for one in all if one["category"] == SpriteCategory.Background]
    preview = [sprite.url for sprite in sprites][randint(0, len(sprites) - 1)]
    comics = Comics(id=file_id, title=title, author=author, url=url, preview=preview) 
    sprite = await firestore.create(collection=Collection.Comics, data=comics.model_dump())
    return Comics(**sprite)

@router.post("/{id}/like")
async def like(id: str) -> Comics:
    comics = await firestore.get_one(collection=Collection.Comics, id=id)
    comics["likes"] = comics["likes"] + 1
    liked = await firestore.update(id=id, collection=Collection.Comics, data=comics)
    return Comics(**liked)