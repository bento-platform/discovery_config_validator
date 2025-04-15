from bento_lib.discovery import DiscoveryConfig
from pydantic import BaseModel, Field
from typing import NotRequired, TypedDict


class ReducedErrorDetails(TypedDict):
    loc: NotRequired[tuple[int | str, ...]]
    msg: str


class ValidationResponse(BaseModel):
    errors: list[ReducedErrorDetails] = []
    warnings: list[ReducedErrorDetails] = []
    config: DiscoveryConfig | None = None
    ok: bool = Field(default_factory=lambda d: len(d.get("errors", [])) == 0 and d.get("config") is not None)
