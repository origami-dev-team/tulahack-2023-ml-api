from fastapi import FastAPI
from constants import Collection
from sprite.router import router as sprite_router
from user.router import router as user_router
from comics.router import router as comics_router

# RUN FROM /home/tcaty/api/src/
# by uvicorn src.main:app --host 0.0.0.0 --port 3000 --reload
app = FastAPI()

app.include_router(sprite_router, prefix=f"/{Collection.Sprite}")
app.include_router(user_router, prefix=f"/{Collection.User}")
app.include_router(comics_router, prefix=f"/{Collection.Comics}")
