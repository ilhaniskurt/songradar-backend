from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.sql import crud, models, schemas
from app.utils import dependencies

router = APIRouter(prefix="/starred", tags=["starred"])


@router.put("/{id}", response_model=list[schemas.Song])
def star_a_song(
    current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
    id: str,
    db: Session = Depends(dependencies.get_db),
):
    return crud.star_song(db, id, current_user.id).songs


@router.delete("/{id}", response_model=list[schemas.Song])
def unstar_a_song(
    current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
    id: str,
    db: Session = Depends(dependencies.get_db),
):
    return crud.unstar_song(db, id, current_user.id).songs


@router.get("/", response_model=list[schemas.Song])
def read_starred(
    current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
    db: Session = Depends(dependencies.get_db),
):
    return crud.get_starred(db, current_user.id).songs
