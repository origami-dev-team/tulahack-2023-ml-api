from typing import List
from fastapi import APIRouter, UploadFile
from constants import SpriteCategory, Collection
from .models import GenerateSpriteDTO, Sprite
from database import firestore
from utils import generate_image, id
from torch import load

model = load("models/model.pth")
router = APIRouter()

@router.get("/{category}")
async def get(category: SpriteCategory) -> List[str]:
    all = await firestore.get_all(collection=Collection.Sprite)
    sprites = [Sprite(**one) for one in all if one["category"] == category]
    urls = [sprite.url for sprite in sprites]
    return urls

@router.post("/{category}")
async def generate(category: SpriteCategory, generate_sprite_dto: GenerateSpriteDTO) -> List[str]:
    images = generate_image(
        query=generate_sprite_dto.prompt, 
        model=model, 
        generate_emotions=category == SpriteCategory.Character,
        delete_background=category == SpriteCategory.Character
    )
    urls = []
    for image in images:
        file_id = id()
        image = UploadFile(file=image, filename=category)
        url = await firestore.upload_file(file=image, folder=category, id=file_id, from_string=True)
        sprite = Sprite(id=file_id, category=category, url=url)
        sprite = await firestore.create(collection=Collection.Sprite, data=sprite.model_dump())
        urls.append(url)
    return urls