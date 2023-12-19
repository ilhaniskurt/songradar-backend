from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.sql import crud, schemas
from app.utils import dependencies

router = APIRouter(prefix="/songs", tags=["songs"])


@router.get("/", response_model=list[schemas.Song])
def read_songs(
    skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db)
):
    songs = crud.get_songs(db, skip=skip, limit=limit)
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


@router.get("/{id}", response_model=schemas.Song)
def get_song_by_id(id: str, db: Session = Depends(dependencies.get_db)):
    song = crud.get_song_by_id(db, id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


@router.get("/count")
def song_count(db: Session = Depends(dependencies.get_db)):
    return crud.get_song_count(db)
