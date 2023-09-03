import os

import yaml
from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SENTRY_DSN: HttpUrl | None = None
    ENV: str | None = None
    BASE_DIR: str
    OPENAI_API_KEY: str

    class Config:
        case_sensitive = True


def read_yaml(file_path: str) -> Settings:
    with open(file_path) as stream:
        config = yaml.safe_load(stream)

    return Settings(**config)
