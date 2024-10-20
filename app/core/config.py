from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = ''

    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///db.sqlite3'


settings = Settings()
