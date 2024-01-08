from sqlalchemy import Boolean, Column, Float, Integer, String
from sqlalchemy.inspection import inspect

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Song(Base):
    __tablename__ = "songs"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    album = Column(String, index=True)
    album_id = Column(String, index=True)
    artists = Column(String, index=True)
    artist_ids = Column(String, index=True)
    track_number = Column(Integer)
    disc_number = Column(Integer)
    explicit = Column(Boolean)
    danceability = Column(Float)
    energy = Column(Float)
    key = Column(Integer)
    loudness = Column(Float)
    mode = Column(Integer)
    speechiness = Column(Float)
    acousticness = Column(Float)
    instrumentalness = Column(Float)
    liveness = Column(Float)
    valence = Column(Float)
    tempo = Column(Float)
    duration_ms = Column(Integer)
    time_signature = Column(Integer)
    year = Column(Integer, index=True)
    month = Column(Integer, index=True)
    day = Column(Integer, index=True)

    owner_id = Column(Integer, index=True)


class Album(Base):
    __tablename__ = "albums"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    artists = Column(String, index=True)
    artist_ids = Column(String, index=True, nullable=True)
    number_of_tracks = Column(Integer)
    explicit = Column(Boolean, nullable=True)
    danceability = Column(Float, nullable=True)
    energy = Column(Float, nullable=True)
    key = Column(Integer, nullable=True)
    loudness = Column(Float, nullable=True)
    mode = Column(Integer, nullable=True)
    speechiness = Column(Float, nullable=True)
    acousticness = Column(Float, nullable=True)
    instrumentalness = Column(Float, nullable=True)
    liveness = Column(Float, nullable=True)
    valence = Column(Float, nullable=True)
    tempo = Column(Float, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    time_signature = Column(Integer, nullable=True)
    year = Column(Integer, index=True)
    month = Column(Integer, index=True)
    day = Column(Integer, index=True)

    owner_id = Column(Integer, index=True)

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
