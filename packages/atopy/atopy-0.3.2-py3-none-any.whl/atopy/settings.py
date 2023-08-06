from pydantic import (  # pylint: disable=no-name-in-module
    BaseModel,
    BaseSettings,
)

IModel = BaseModel


class ISettings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
