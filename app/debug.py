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


# Song Debug


@router.get("/songs", response_model=list[schemas.Song])
def read_songs(
    skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)
):
    songs = crud.get_songs(db, skip=skip, limit=limit)
    return songs


@router.post("/songs", response_model=schemas.Song)
def create_song(song: schemas.SongCreate, db: Session = Depends(dependencies.get_db)):
    return crud.create_song(db, song)
