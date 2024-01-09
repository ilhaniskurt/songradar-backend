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


@router.post("/albums", response_model=schemas.AlbumDebug)
def create_album(album: schemas.AlbumDebug, db: Session = Depends(dependencies.get_db)):
    return crud.create_album_debug(db, album)


# Song Debug


@router.post("/songs", response_model=schemas.SongDebug)
def create_song(song: schemas.SongDebug, db: Session = Depends(dependencies.get_db)):
    return crud.create_song_debug(db, song)


# Playlist Debug


@router.get("/playlists", response_model=list[schemas.Playlist])
def read_playlists(
    skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db)
):
    album = crud.get_playlists(db, skip, limit)
    return album
