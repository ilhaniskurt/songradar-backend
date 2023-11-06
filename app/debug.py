from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.sql import crud, schemas
from app.utils import dependencies

router = APIRouter(prefix="/debug", tags=["debug"])


@router.get("/users", response_model=list[schemas.User])
def read_users(
    skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/unsecure")
def read_users_unsecure(
    skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user_by_id(user_id: int, db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
