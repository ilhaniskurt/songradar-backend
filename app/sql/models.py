from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


album_performer_association = Table(
    "album_performer",
    Base.metadata,
    Column("album_id", ForeignKey("albums.id"), primary_key=True),
    Column("performer_id", ForeignKey("performers.id"), primary_key=True),
)


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    # Establish the many-to-many relationship between albums and performers
    performers = relationship(
        "Performer", secondary=album_performer_association, back_populates="albums"
    )
    year = Column(Integer, index=True)
    genre = Column(String, index=True)

    songs = relationship("Song", back_populates="album")


song_performer_association = Table(
    "song_performer",
    Base.metadata,
    Column("song_id", ForeignKey("songs.id"), primary_key=True),
    Column("performer_id", ForeignKey("performers.id"), primary_key=True),
)


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    # Establish the many-to-many relationship between songs and performers
    performers = relationship(
        "Performer", secondary=song_performer_association, back_populates="songs"
    )
    year = Column(Integer, index=True)
    genre = Column(String, index=True)
    album_id = Column(Integer, ForeignKey("albums.id"))

    album = relationship("Album", back_populates="songs")


class Performer(Base):
    __tablename__ = "performers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    # Establish the many-to-many relationship to albums and songs
    albums = relationship(
        "Album", secondary=album_performer_association, back_populates="performers"
    )
    songs = relationship(
        "Song", secondary=song_performer_association, back_populates="performers"
    )
