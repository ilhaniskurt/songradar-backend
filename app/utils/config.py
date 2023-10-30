from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str = "1724d11d6c8983d289b042a04b1fb8b0a5ff89f6613eaf7e364d4331981ea90f"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    sqlalchemy_database_url: str = "sqlite:///./sql.db"


settings = Settings()
