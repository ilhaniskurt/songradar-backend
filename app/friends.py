from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.sql import crud, models, schemas
from app.utils import dependencies

router = APIRouter(prefix="/friends", tags=["friends"])


@router.get("/", response_model=list[schemas.User])
def get_friends(
    current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
    db: Session = Depends(dependencies.get_db),
):
    return crud.get_user(db, current_user.id).friends


@router.post("/send/{id}", response_model=schemas.FriendRequest)
def send_friend_request(
    current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
    id: int,
    db: Session = Depends(dependencies.get_db),
):
    if id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot send a request to self")

    return crud.send_friend_request(db, current_user.id, id)


@router.get("/requests", response_model=list[schemas.FriendRequest])
def get_friend_requests(
    current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
    db: Session = Depends(dependencies.get_db),
):
    return crud.get_friend_requests(db, current_user.id)


@router.get("/requests/pending", response_model=list[schemas.FriendRequest])
def get_pending_friend_requests(
    current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
    db: Session = Depends(dependencies.get_db),
):
    return crud.get_pending_friend_requests(db, current_user.id)


@router.put("/requests/{id}", response_model=schemas.FriendRequest)
def accept_friend_request(
    current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
    id: int,
    db: Session = Depends(dependencies.get_db),
):
    request = crud.accept_friend_request(db, id, current_user.id)
    if not request:
        raise HTTPException(status_code=400, detail="Invalid request id " + str(id))
    return request


@router.delete("/requests/{id}", response_model=schemas.FriendRequest)
def reject_friend_request(
    current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
    id: int,
    db: Session = Depends(dependencies.get_db),
):
    request = crud.deny_friend_request(db, id, current_user.id)
    if not request:
        raise HTTPException(status_code=400, detail="Invalid request id " + str(id))
    return request
