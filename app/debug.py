from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.sql import crud, schemas
from app.utils import dependencies

router = APIRouter(prefix="/debug", tags=["debug"])

# User Debug


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


# Album Debug


@router.get("/albums", response_model=list[schemas.Album])
def read_albums(
    skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)
):
    albums = crud.get_albums(db, skip=skip, limit=limit)
    return albums


@router.post("/album", response_model=schemas.Album)
def create_album(
    album: schemas.AlbumCreate, db: Session = Depends(dependencies.get_db)
):
    return crud.create_album(db, album)


# Performer Debug


@router.get("/performer", response_model=list[schemas.Performer])
def read_performers(
    skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)
):
    performers = crud.get_performers(db, skip=skip, limit=limit)
    return performers


@router.get("/performer/{performer_id}", response_model=schemas.Performer)
def read_performer_by_id(performer_id: int, db: Session = Depends(dependencies.get_db)):
    db_performer = crud.get_performer(db, performer_id)
    if db_performer is None:
        raise HTTPException(status_code=404, detail="Performer not found")
    return db_performer


@router.post("/performer", response_model=schemas.Performer)
def create_performer(
    performer: schemas.PerformerCreate, db: Session = Depends(dependencies.get_db)
):
    return crud.create_performer(db, performer)
