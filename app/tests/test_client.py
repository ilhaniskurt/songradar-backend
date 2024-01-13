from functools import lru_cache

from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.sql.database import Base
from app.utils.dependencies import get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def create_user(username: str, password: str, email: str):
    response = client.post(
        "/auth/sign_up",
        headers={"accept": "application/json", "Content-Type": "application/json"},
        json={"username": username, "password": password, "email": email},
    )
    if response.status_code != 200:
        raise Exception("User creating failed!")


@lru_cache
def get_auth_header(username: str, password: str, email: str):
    create_user(username, password, email)
    response = client.post(
        "/auth/sign_in",
        headers={"accept": "application/json"},
        data={"username": username, "password": password},
    )
    data = response.json()
    header = {
        "Authorization": "Bearer " + data["access_token"],
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    return header


@fixture(scope="session")
def auth_headers():
    user_1 = get_auth_header("ilanya", "Ilhan.1234", "ilhan@gmail.com")
    user_2 = get_auth_header("yavuzil", "Yavuz.1234", "yavuz@gmail.com")

    yield [user_1, user_2]
