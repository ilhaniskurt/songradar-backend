from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.sql import crud, models, schemas
from app.utils import dependencies, security

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/sign_in", response_model=security.Token)
async def sign_in(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(dependencies.get_db),
):
    user = crud.get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = security.create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/sign_up", response_model=schemas.User)
def sign_up(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username is taken")
    return crud.create_user(db=db, user=user)


@router.get("/me", response_model=schemas.User)
async def read_current_user(
    current_user: Annotated[models.User, Depends(dependencies.get_current_user)]
):
    return current_user
