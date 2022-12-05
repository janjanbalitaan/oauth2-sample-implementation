from pydantic import (
    BaseSettings,
    Field,
)
from typing import Optional


class Settings(BaseSettings):
    app_name: str = Field(env="APP_NAME")
    app_description: str = Field(env="APP_DESC")
    app_version: str = Field(env="APP_VERSION")
    db_uri: str = Field(env="DB_URI")
    secret_key: str = Field(env="SECRET_KEY")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True
