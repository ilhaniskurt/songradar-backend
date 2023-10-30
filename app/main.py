from fastapi import FastAPI

from app.auth import router as auth_router
from app.sql import database, models
from app.users import router as users_router

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(auth_router)
app.include_router(users_router)
