from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):

    # Databse Info
    TYPE_DB: str
    HOST_DB: str
    DATABASE_NAME: str
    PORT_DB: int
    USER_DB: str
    PASSWORD_DB: str

    # Token Info
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Origin Info
    FRONTEND: str
    BACKEND: str

    # Email Info
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    LOGO_PATH: str

    # Initial User Info
    NAME_USER: str
    USERNAME_USER: str
    EMAIL_USER: str
    TEMP_PASS: str
    LENGTH_TEMP_PASS: int

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()