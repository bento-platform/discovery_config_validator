from pathlib import Path
from pydantic_settings import BaseSettings

__all__ = ["Config", "config"]


class Config(BaseSettings):
    serve_client: bool = False
    client_path: Path = Path()  # TODO: default


config = Config()
