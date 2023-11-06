from sqlalchemy.orm import Session

from ..utils import security
from . import models, schemas

# User CRUD


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        **user.model_dump(exclude="password"),
        hashed_password=security.get_password_hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Album CRUD


def get_albums(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Album).offset(skip).limit(limit).all()


def create_album(db: Session, album: schemas.AlbumCreate):
    db_album = models.Album(**album.model_dump())
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album


# Song CRUD


def get_songs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Song).offset(skip).limit(limit).all()


def create_song(db: Session, song: schemas.SongCreate):
    db_song = models.Song(**song.model_dump())
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song
