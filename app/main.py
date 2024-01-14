from fastapi import FastAPI

from app.albums import router as albums_router
from app.auth import router as auth_router
from app.debug import router as debug_router
from app.playlists import router as playlists_router
from app.recommend import recommend_lifespan
from app.recommend import router as recommend_router
from app.songs import router as songs_router
from app.sql import database, models
from app.starred import router as starred_router
from app.utils.config import settings

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(lifespan=recommend_lifespan)
app.include_router(auth_router)
app.include_router(songs_router)
app.include_router(albums_router)
app.include_router(playlists_router)
app.include_router(starred_router)
app.include_router(recommend_router)
if settings.debug_mode:
    app.include_router(debug_router)
