from fastapi import APIRouter
from .models import CreateUserDTO, User
from database import firestore
from constants import Collection

router = APIRouter()

@router.post("/")
async def create(create_user_dto: CreateUserDTO) -> User:
    user = User(**create_user_dto.model_dump(), id=create_user_dto.username)
    user = await firestore.create(collection=Collection.User, data=user.model_dump(), unique=True)
    return User(**user)

    
@router.get("/{username}")
async def get_one(username: str) -> User:
    user = await firestore.get_one(collection=Collection.User, id=username)
    return User(**user)