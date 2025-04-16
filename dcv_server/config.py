from pathlib import Path
from pydantic_settings import BaseSettings

__all__ = ["Config", "config"]


class Config(BaseSettings):
    serve_client: bool = True
    client_path: Path = Path(__file__).parent.parent / "dcv_client" / "dist"


config = Config()
