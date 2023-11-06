from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    performers = Column(String, index=True)
    year = Column(Integer, index=True)
    genre = Column(String, index=True)

    songs = relationship("Song", back_populates="album", cascade="all, delete-orphan")


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    performers = Column(String, index=True)
    year = Column(Integer, index=True)
    genre = Column(String, index=True)

    album_id = Column(Integer, ForeignKey("albums.id"))
    album = relationship("Album", back_populates="songs")
