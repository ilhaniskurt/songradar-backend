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


# Song CRUD


def get_songs(db: Session, skip: int, limit: int):
    return db.query(models.Song).offset(skip).limit(limit).all()


def get_song_by_id(db: Session, id: str):
    return db.query(models.Song).filter(models.Song.id == id).first()


def get_songs_by_album_id(db: Session, album_id: str):
    return db.query(models.Song).filter(models.Song.album_id == album_id).all()


def search_songs_by_name(db: Session, name: str, skip: int, limit: int):
    return (
        db.query(models.Song)
        .filter(models.Song.name.ilike(f"%{name}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )


def search_songs_by_artist(db: Session, artist: str, skip: int, limit: int):
    return (
        db.query(models.Song)
        .filter(models.Song.artists.ilike(f"%{artist}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_song_debug(db: Session, song: schemas.SongDebug):
    db_song = models.Song(**song.model_dump())
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song


def get_song_count(db: Session):
    return db.query(models.Song).count()


# Album CRUD


def get_albums(db: Session, skip: int, limit: int):
    return db.query(models.Album).offset(skip).limit(limit).all()


def get_album_by_id(db: Session, id: str):
    return db.query(models.Album).filter(models.Album.id == id).first()


def search_albums_by_name(db: Session, name: str, skip: int, limit: int):
    return (
        db.query(models.Album)
        .filter(models.Album.name.ilike(f"%{name}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )


def search_albums_by_artist(db: Session, artist: str, skip: int, limit: int):
    return (
        db.query(models.Album)
        .filter(models.Album.artists.ilike(f"%{artist}%"))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_album_debug(db: Session, album: schemas.AlbumDebug):
    db_song = models.Album(**album.model_dump())
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song


def get_album_count(db: Session):
    return db.query(models.Album).count()
