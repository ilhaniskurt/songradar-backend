from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.sql import crud, models, schemas
from app.utils import dependencies

router = APIRouter(prefix="/playlists", tags=["playlists"])


@router.post("/", response_model=schemas.Playlist)
def create_playlist(
    current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
    playlist: schemas.PlaylistCreate,
    db: Session = Depends(dependencies.get_db),
):
    return crud.create_playlist(db, playlist, current_user.id)


@router.delete("/{id}")
def delete_playlist(
    current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
    id: str,
    db: Session = Depends(dependencies.get_db),
):
    crud.delete_playlist(db, id, current_user.id)
    return True


@router.put("/{id}", response_model=schemas.Playlist)
def rename_playlist(
    current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
    id: int,
    new_name: str,
    db: Session = Depends(dependencies.get_db),
):
    return crud.update_playlist_name(db, id, current_user.id, new_name)


@router.put("/{id}/{song_id}", response_model=schemas.Playlist)
def add_to_playlist(
    current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
    id: int,
    song_id: str,
    db: Session = Depends(dependencies.get_db),
):
    return crud.add_song_to_playlist(db, id, song_id, current_user.id)


@router.delete("/{id}/{song_id}", response_model=schemas.Playlist)
def remove_from_playlist(
    current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
    id: int,
    song_id: str,
    db: Session = Depends(dependencies.get_db),
):
    return crud.remove_song_from_playlist(db, id, song_id, current_user.id)


@router.get("/user", response_model=list[schemas.Playlist])
def read_user_playlists(
    current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(dependencies.get_db),
):
    playlist = crud.get_playlists_by_owner_id(db, current_user.id, skip, limit)
    return playlist


@router.get("/{id}", response_model=schemas.Playlist)
def get_playlist_by_id(id: str, db: Session = Depends(dependencies.get_db)):
    playlist = crud.get_playlist_by_id(db, id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")

    return playlist
