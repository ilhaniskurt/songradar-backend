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
    db_starred = models.Starred(id=db_user.id)
    db.add(db_user)
    db.add(db_starred)
    db.commit()
    db.refresh(db_user)
    return db_user


# Song CRUD


def get_song_count(db: Session):
    return db.query(models.Song).count()


def get_songs(db: Session, skip: int, limit: int):
    return db.query(models.Song).offset(skip).limit(limit).all()


def get_all_defualt_songs(db: Session):
    return db.query(models.Song).filter(models.Song.owner_id == 0).all()


def get_songs_recent(db: Session, skip: int, limit: int):
    count = get_song_count(db)
    return reversed(
        db.query(models.Song).offset(count - limit - skip).limit(limit).all()
    )


def get_songs_by_owner_id(db: Session, owner_id: str, skip: int, limit: int):
    return (
        db.query(models.Song)
        .filter(models.Song.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
        .all()
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
            status_code=400,
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
            status_code=400,
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


def get_albums_by_owner_id(db: Session, owner_id: str, skip: int, limit: int):
    return (
        db.query(models.Album)
        .filter(models.Album.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
        .all()
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
            status_code=400,
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


# Playlist CRUD


def create_playlist(db: Session, playlist: schemas.PlaylistCreate, owner_id: int):
    new_playlist = models.Playlist(**playlist.model_dump(), owner_id=owner_id)
    db.add(new_playlist)
    db.commit()
    db.refresh(new_playlist)
    return new_playlist


def get_playlist_by_id(db: Session, id: int):
    return db.query(models.Playlist).filter(models.Playlist.id == id).first()


def get_playlists_by_owner_id(db: Session, owner_id: int, skip: int, limit: int):
    return (
        db.query(models.Playlist)
        .filter(models.Playlist.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_playlist_name(db: Session, id: int, owner_id: int, new_name: str):
    playlist = db.query(models.Playlist).filter(models.Playlist.id == id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail=f"Invalid playlist id: {id}")

    if playlist.owner_id != owner_id:
        raise HTTPException(
            status_code=400,
            detail="Cannot change the name of a playlist that does not belong to you",
        )

    playlist.name = new_name
    db.commit()
    db.refresh(playlist)
    return playlist


def delete_playlist(db: Session, id: int, owner_id: int):
    playlist = db.query(models.Playlist).filter(models.Playlist.id == id).first()

    if not playlist:
        raise HTTPException(status_code=404, detail=f"Invalid playlist id: {id}")

    if playlist.owner_id != owner_id:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete a playlist that does not belong to you",
        )

    db.delete(playlist)
    db.commit()
    return True


def add_song_to_playlist(db: Session, id: int, song_id: str, owner_id: str):
    playlist = db.query(models.Playlist).filter(models.Playlist.id == id).first()

    if not playlist:
        raise HTTPException(status_code=404, detail=f"Invalid playlist id: {id}")

    if playlist.owner_id != owner_id:
        raise HTTPException(
            status_code=400,
            detail="Cannot add a song to a playlist that does not belong to you",
        )

    song = db.query(models.Song).filter(models.Song.id == song_id).first()

    if not song:
        raise HTTPException(status_code=404, detail=f"Invalid song id: {song_id}")

    if song in playlist.songs:
        raise HTTPException(
            status_code=400,
            detail="Song is already in the playlist",
        )

    playlist.songs.append(song)
    db.commit()
    db.refresh(playlist)
    return playlist


def remove_song_from_playlist(db: Session, id: int, song_id: str, owner_id: int):
    playlist = db.query(models.Playlist).filter(models.Playlist.id == id).first()

    if not playlist:
        raise HTTPException(status_code=404, detail=f"Invalid playlist id: {id}")

    if playlist.owner_id != owner_id:
        raise HTTPException(
            status_code=400,
            detail="Cannot remove a song from a playlist that does not belong to you",
        )

    song = db.query(models.Song).filter(models.Song.id == song_id).first()

    if not song:
        raise HTTPException(status_code=404, detail=f"Invalid song id: {song_id}")

    if song not in playlist.songs:
        raise HTTPException(
            status_code=400,
            detail="Song is not in the playlist",
        )

    playlist.songs.remove(song)
    db.commit()
    db.refresh(playlist)
    return playlist


def get_playlists(db: Session, skip: int, limit: int):
    return db.query(models.Playlist).offset(skip).limit(limit).all()


# Starred Debug


def is_starred(db: Session, id: str, owner_id: str):
    starred = db.query(models.Starred).filter(models.Starred.id == owner_id).first()

    if not starred:
        raise HTTPException(status_code=404, detail=f"Invalid user id: {owner_id}")

    song = db.query(models.Song).filter(models.Song.id == id).first()

    if not song:
        raise HTTPException(status_code=404, detail=f"Invalid song id: {id}")

    return song in starred.songs


def star_song(db: Session, id: str, owner_id: str):
    starred = db.query(models.Starred).filter(models.Starred.id == owner_id).first()

    if not starred:
        raise HTTPException(status_code=404, detail=f"Invalid user id: {owner_id}")

    song = db.query(models.Song).filter(models.Song.id == id).first()

    if not song:
        raise HTTPException(status_code=404, detail=f"Invalid song id: {id}")

    if song in starred.songs:
        raise HTTPException(
            status_code=400,
            detail="Song is already starred",
        )

    starred.songs.append(song)
    db.commit()
    db.refresh(starred)
    return starred


def unstar_song(db: Session, id: str, owner_id: int):
    starred = db.query(models.Starred).filter(models.Starred.id == owner_id).first()

    if not starred:
        raise HTTPException(status_code=404, detail=f"Invalid user id: {owner_id}")

    song = db.query(models.Song).filter(models.Song.id == id).first()

    if not song:
        raise HTTPException(status_code=404, detail=f"Invalid song id: {id}")

    if song not in starred.songs:
        raise HTTPException(
            status_code=400,
            detail="Song is not starred",
        )

    starred.songs.remove(song)
    db.commit()
    db.refresh(starred)
    return starred


def get_starred(db: Session, owner_id: int):
    return db.query(models.Starred).filter(models.Starred.id == owner_id).first()


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
