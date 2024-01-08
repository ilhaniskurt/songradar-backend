from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.sql import crud, models, schemas
from app.utils import dependencies

router = APIRouter(prefix="/albums", tags=["albums"])


@router.delete("/{id}")
def delete_album(
    current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
    id: str,
    db: Session = Depends(dependencies.get_db),
):
    crud.delete_album(db, id, current_user.id)
    return True


@router.post("/", response_model=schemas.Album)
def create_album(
    current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
    song: schemas.AlbumCreate,
    db: Session = Depends(dependencies.get_db),
):
    return crud.create_album(db, song, current_user.id)


@router.get("/user", response_model=list[schemas.Album])
def read_user_albums(
    current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(dependencies.get_db),
):
    album = crud.get_albums_by_owner_id(db, current_user.id, skip, limit)
    return album


@router.get("/", response_model=list[schemas.Album])
def read_albums(
    skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db)
):
    album = crud.get_albums(db, skip, limit)
    return album


@router.get("/recent", response_model=list[schemas.Album])
def read_albums_recent(
    skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db)
):
    album = crud.get_albums_recent(db, skip, limit)
    return album


@router.get("/search_name", response_model=list[schemas.Album])
def search_album_by_name(
    name: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(dependencies.get_db),
):
    return crud.search_albums_by_name(db, name, skip, limit)


@router.get("/search_artist", response_model=list[schemas.Album])
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


@router.get("/find/{album_id}", response_model=schemas.AlbumPopulated)
def get_album_with_tracks_by_id(
    album_id: str, db: Session = Depends(dependencies.get_db)
):
    album = crud.get_album_by_id(db, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    tracks = crud.get_songs_by_album_id(db, album_id)
    return schemas.AlbumPopulated(**album.to_dict(), tracks=tracks)
