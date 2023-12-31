from random import randint
from fastapi import APIRouter, UploadFile, Form
from database import firestore
from typing import Annotated, List
from .models import Comics
from sprite.models import Sprite
from utils import id
from constants import Collection, SpriteCategory
from datetime import datetime

router = APIRouter()

@router.get("")
async def get_all() -> List[Comics]:
    all = await firestore.get_all(collection=Collection.Comics)
    return [Comics(**one) for one in all]

@router.post("")
async def upload(title: Annotated[str, Form()], author: Annotated[str, Form()], file: UploadFile) -> Comics:
    file_id = id()
    file.filename = title.replace(" ", "-") + '-' + str(file.filename)
    url = await firestore.upload_file(file=file, folder=Collection.Comics, id=file_id)
    all = await firestore.get_all(collection=Collection.Sprite)
    sprites = [Sprite(**one) for one in all if one["category"] == SpriteCategory.Background]
    sprites = list(sorted(sprites, key=lambda sprite: datetime.fromisoformat(str(sprite.created_at)).timestamp()))
    preview = [sprite.url for sprite in sprites][-1]
    await firestore.create(collection=Collection.Preview, data={"url": preview, "id": file_id})
    comics = Comics(id=file_id, title=title, author=author, url=url, preview=preview) 
    sprite = await firestore.create(collection=Collection.Comics, data=comics.model_dump())
    return Comics(**sprite)

@router.post("/{id}/like")
async def like(id: str) -> Comics:
    comics = await firestore.get_one(collection=Collection.Comics, id=id)
    comics["likes"] = comics["likes"] + 1
    liked = await firestore.update(id=id, collection=Collection.Comics, data=comics)
    return Comics(**liked)