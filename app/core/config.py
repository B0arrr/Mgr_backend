import secrets

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = ''

    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///db.sqlite3'

    API_V1_STR: str = '/api/v1'

    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    SUPERUSER_EMAIL: str = 'admin@admin.com'
    SUPERUSER_PASSWORD: str = 'Admin123!'

    OPEN_API_KEY: str = ''


settings = Settings()
