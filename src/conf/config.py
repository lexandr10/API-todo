from pydantic_settings import BaseSettings
from pydantic import ConfigDict, EmailStr


class Settings(BaseSettings):
    DB_URL: str = (
        "postgres+asyncpg://postgres:alexandrenko2707@localhost:5432/todo_app",
    )
    # jwt
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    # redis
    REDIS_URL: str = "redis://localhost"
    # mail
    MAIL_USERNAME: str = "fd8728bdb0c2a5"
    MAIL_PASSWORD: str = "secretPassword"
    MAIL_FROM: EmailStr = "example@meta.ua"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.meta.ua"
    MAIL_FROM_NAME: str = "Rest API Service"
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = True
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    # cloudinary
    CLD_NAME: str = "cloudinary_name"
    CLD_API_KEY: str = "cloudinary_api_key"
    CLD_API_SECRET: str = "cloudinary_api_secret"

    model_config = ConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )


settings = Settings()
