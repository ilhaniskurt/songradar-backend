from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.sql import crud, models, schemas
from app.utils import dependencies

router = APIRouter(prefix="/songs", tags=["songs"])


@router.post("/", response_model=schemas.Song)
def create_song(
    current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
    song: schemas.SongCreate,
    db: Session = Depends(dependencies.get_db),
):
    return crud.create_song(db, song, current_user.id)


@router.get("/", response_model=list[schemas.Song])
def read_songs(
    skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db)
):
    songs = crud.get_songs(db, skip=skip, limit=limit)
    return songs


@router.get("/recent", response_model=list[schemas.Song])
def read_songs_recent(
    skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db)
):
    songs = crud.get_songs_recent(db, skip=skip, limit=limit)
    return songs


@router.get("/search_name", response_model=list[schemas.Song])
def search_song_by_name(
    name: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(dependencies.get_db),
):
    return crud.search_songs_by_name(db, name, skip, limit)


@router.get("/search_artist", response_model=list[schemas.Song])
def search_songs_by_artist(
    artist: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(dependencies.get_db),
):
    return crud.search_songs_by_artist(db, artist, skip, limit)


@router.get("/count")
def song_count(db: Session = Depends(dependencies.get_db)):
    return crud.get_song_count(db)


@router.get("/find/{id}", response_model=schemas.Song)
def get_song_by_id(id: str, db: Session = Depends(dependencies.get_db)):
    song = crud.get_song_by_id(db, id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song
