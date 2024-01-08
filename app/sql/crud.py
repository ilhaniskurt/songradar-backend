from uuid import uuid4

from fastapi import HTTPException
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


def get_song_count(db: Session):
    return db.query(models.Song).count()


def get_songs(db: Session, skip: int, limit: int):
    return db.query(models.Song).offset(skip).limit(limit).all()


def get_songs_recent(db: Session, skip: int, limit: int):
    count = get_song_count(db)
    return reversed(
        db.query(models.Song).offset(count - limit - skip).limit(limit).all()
    )


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


def delete_song(db: Session, id: str, owner_id: int):
    song = db.query(models.Song).filter(models.Song.id == id).first()

    if not song:
        raise HTTPException(status_code=404, detail=f"Invalid song id: {id}")

    if song.owner_id != owner_id:
        raise HTTPException(
            status_code=404,
            detail="Cannot delete a song that is not registered by you",
        )

    album = db.query(models.Album).filter(models.Album.id == song.album_id).first()

    album.number_of_tracks -= 1
    db.delete(song)
    db.commit()
    db.refresh(album)


def create_song(db: Session, song: schemas.SongCreate, owner_id: int):
    q = db.query(models.Album).filter(models.Album.id == song.album_id).first()

    if not q:
        raise HTTPException(
            status_code=404, detail=f"Invalid album id: {song.album_id}"
        )

    if q.owner_id != owner_id:
        raise HTTPException(
            status_code=404,
            detail="Cannot add a song to an album that is not registered by you",
        )

    q.number_of_tracks += 1
    db_song = models.Song(
        **song.model_dump(), id=str(uuid4()), owner_id=owner_id, album=q.name
    )
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song


# Album CRUD


def get_album_count(db: Session):
    return db.query(models.Album).count()


def get_albums(db: Session, skip: int, limit: int):
    return db.query(models.Album).offset(skip).limit(limit).all()


def get_albums_recent(db: Session, skip: int, limit: int):
    count = get_album_count(db)
    return reversed(
        db.query(models.Album).offset(count - limit - skip).limit(limit).all()
    )


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


def delete_album(db: Session, id: str, owner_id: int):
    album = db.query(models.Album).filter(models.Album.id == id).first()

    if not album:
        raise HTTPException(status_code=404, detail=f"Invalid album id: {id}")

    if album.owner_id != owner_id:
        raise HTTPException(
            status_code=404,
            detail="Cannot delete a album that is not registered by you",
        )

    for song in get_songs_by_album_id(db, id):
        db.delete(song)

    db.delete(album)
    db.commit()


def create_album(db: Session, album: schemas.AlbumCreate, owner_id: int):
    db_song = models.Album(
        **album.model_dump(), id=str(uuid4()), owner_id=owner_id, number_of_tracks=0
    )
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song


# Debug


def create_song_debug(db: Session, song: schemas.SongDebug):
    db_song = models.Song(**song.model_dump())
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song


def create_album_debug(db: Session, album: schemas.AlbumDebug):
    db_song = models.Album(**album.model_dump())
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song
