import re
from datetime import datetime

from email_validator import EmailNotValidError, validate_email
from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator

# User Schemas


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str

    @field_validator("*")
    @classmethod
    def check_empty_fields(cls, v: str, info: ValidationInfo):
        if not v:
            raise HTTPException(
                status_code=400, detail="Empty " + info.field_name + " field"
            )
        return v

    @field_validator("username")
    @classmethod
    def check_username(cls, v: str):
        details = []
        if len(v) < 6:
            details.append("Username must be at least 6 characters long.")
        if len(v) > 18:
            details.append("Username must not be more than 18 characters long.")
        if not v.isalnum():
            details.append("Username can only contain alphanumeric characters.")
        if v[0].isdigit():
            details.append("Username cannot start with a number.")
        if details:
            raise HTTPException(status_code=400, detail=details)
        return v

    @field_validator("email")
    @classmethod
    def check_email(cls, v: str):
        try:
            email = validate_email(v)
        except EmailNotValidError as e:
            raise HTTPException(status_code=400, detail="Invalid email: " + str(e))
        return email.normalized

    @field_validator("password")
    @classmethod
    def check_password(cls, v: str):
        details = []
        if len(v) < 8:
            details.append("Password must be at least 8 characters long.")
        if re.search(r"\s", v):
            details.append("Password must not contain any whitespace characters.")
        if not re.search(r"[A-Z]", v):
            details.append("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", v):
            details.append("Password must contain at least one lowercase letter.")
        if not re.search(r"[0-9]", v):
            details.append("Password must contain at least one numeric digit.")
        if not re.search(r"[^A-Za-z0-9]", v):
            details.append("Password must contain at least one special character.")

        if details:
            raise HTTPException(status_code=400, detail=details)
        return v


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Friend Request Schema


class FriendRequest(BaseModel):
    id: int
    requester_id: int
    requester_name: str
    requestee_id: int
    requestee_name: str
    status: str

    model_config = ConfigDict(from_attributes=True)


# Song Schemas


class SongBase(BaseModel):
    name: str
    album_id: str
    artists: str
    year: int
    month: int
    day: int


class SongCreate(SongBase):
    @field_validator("day")
    def validate_date(cls, v, values):
        year = values.data["year"]
        month = values.data["month"]
        day = v
        try:
            date = datetime(year, month, day)
        except ValueError as e:
            raise HTTPException(status_code=400, detail="Invalid date: " + str(e))

        if date > datetime.now():
            raise HTTPException(
                status_code=400,
                detail="Date cannot be in the future: " + str(date.date()),
            )
        if date < datetime(1900, 1, 1):
            raise HTTPException(
                status_code=400,
                detail="Date cannot be before January 1, 1900: " + str(date.date()),
            )
        return v


class Song(SongBase):
    id: str
    album: str
    owner_id: int

    # Nullable
    artist_ids: str | None
    explicit: bool | None
    danceability: float | None
    energy: float | None
    key: int | None
    loudness: float | None
    mode: int | None
    speechiness: float | None
    acousticness: float | None
    instrumentalness: float | None
    liveness: float | None
    valence: float | None
    tempo: float | None
    duration_ms: int | None
    time_signature: int | None

    model_config = ConfigDict(from_attributes=True)


# Album Schemas


class AlbumBase(BaseModel):
    name: str
    artists: str
    year: int
    month: int
    day: int


class AlbumCreate(AlbumBase):
    @field_validator("day")
    def validate_date(cls, v, values):
        year = values.data["year"]
        month = values.data["month"]
        day = v
        try:
            date = datetime(year, month, day)
        except ValueError as e:
            raise HTTPException(status_code=400, detail="Invalid date: " + str(e))

        if date > datetime.now():
            raise HTTPException(
                status_code=400,
                detail="Date cannot be in the future: " + str(date.date()),
            )
        if date < datetime(1900, 1, 1):
            raise HTTPException(
                status_code=400,
                detail="Date cannot be before January 1, 1900: " + str(date.date()),
            )
        return v


class Album(AlbumBase):
    id: str
    owner_id: int

    number_of_tracks: int

    # Nullable
    artist_ids: str | None
    explicit: bool | None
    danceability: float | None
    energy: float | None
    key: int | None
    loudness: float | None
    mode: int | None
    speechiness: float | None
    acousticness: float | None
    instrumentalness: float | None
    liveness: float | None
    valence: float | None
    tempo: float | None
    duration_ms: int | None
    time_signature: int | None

    model_config = ConfigDict(from_attributes=True)


class AlbumPopulated(Album):
    tracks: list[Song]


# Playlist Schemas


class PlaylistBase(BaseModel):
    name: str


class PlaylistCreate(PlaylistBase):
    pass


class Playlist(PlaylistBase):
    id: int
    owner_id: int
    songs: list[Song] | None

    model_config = ConfigDict(from_attributes=True)


# Debug


class SongDebug(BaseModel):
    id: str
    name: str
    album: str
    album_id: str
    artists: str
    artist_ids: str
    track_number: int
    disc_number: int
    explicit: bool
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    duration_ms: int
    time_signature: int
    year: int
    month: int
    day: int

    owner_id: int = 0


class AlbumDebug(BaseModel):
    id: str
    name: str
    artists: str
    artist_ids: str
    number_of_tracks: int
    explicit: bool
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    duration_ms: int
    time_signature: int
    year: int
    month: int
    day: int

    owner_id: int = 0
