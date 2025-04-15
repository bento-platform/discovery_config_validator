from pydantic_settings import BaseSettings

__all__ = ["Config"]


class Config(BaseSettings):
    serve_client_on_404: bool = False
    client_path: str  # TODO
