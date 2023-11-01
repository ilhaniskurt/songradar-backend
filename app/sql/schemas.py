import re

from email_validator import EmailNotValidError, validate_email
from fastapi import HTTPException
from pydantic import BaseModel, ValidationInfo, field_validator


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

    class Config:
        from_attributes = True
