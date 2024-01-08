from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.sql import crud, schemas
from app.utils import dependencies

router = APIRouter(prefix="/albums", tags=["albums"])


@router.get("/", response_model=list[schemas.AlbumBase])
def read_albums(
    skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db)
):
    album = crud.get_albums(db, skip=skip, limit=limit)
    return album


@router.get("/search_name", response_model=list[schemas.AlbumBase])
def search_album_by_name(
    name: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(dependencies.get_db),
):
    return crud.search_albums_by_name(db, name, skip, limit)


@router.get("/search_artist", response_model=list[schemas.AlbumBase])
def search_album_by_artist(
    artist: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(dependencies.get_db),
):
    return crud.search_albums_by_artist(db, artist, skip, limit)


@router.get("/count")
def album_count(db: Session = Depends(dependencies.get_db)):
    return crud.get_album_count(db)


@router.get("/find/{album_id}", response_model=schemas.Album)
def get_album_by_id(album_id: str, db: Session = Depends(dependencies.get_db)):
    album = crud.get_album_by_id(db, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    tracks = crud.get_songs_by_album_id(db, album_id)
    return schemas.Album(**album.to_dict(), tracks=tracks)
