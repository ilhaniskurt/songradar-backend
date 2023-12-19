import re

from email_validator import EmailNotValidError, validate_email
from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator


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


class SongBase(BaseModel):
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


class SongCreate(SongBase):
    pass


class Song(SongBase):
    model_config = ConfigDict(from_attributes=True)


class AlbumBase(BaseModel):
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


class AlbumCreate(AlbumBase):
    pass


class Album(AlbumBase):
    tracks: list[Song]

    model_config = ConfigDict(from_attributes=True)
