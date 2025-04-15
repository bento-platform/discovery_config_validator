import orjson
from bento_lib.discovery import DiscoveryConfig, load_discovery_config_from_dict
from fastapi import FastAPI, File
from pydantic import ValidationError
from typing import Annotated

from .types import ValidationResponse
from .utils import reduce_error_details, warning_to_reduced_error_details

app = FastAPI()


@app.post("/api/v1/validate")
async def validate_config(file: Annotated[bytes, File()]) -> ValidationResponse:
    try:
        data = orjson.loads(file)
    except orjson.JSONDecodeError:
        return ValidationResponse(errors=[{"msg": "JSON decode error"}])

    config: DiscoveryConfig
    try:
        config, warnings = load_discovery_config_from_dict(data)
    except ValidationError as e:
        e: ValidationError
        return ValidationResponse(errors=[reduce_error_details(err) for err in e.errors()])

    return ValidationResponse(config=config, warnings=[warning_to_reduced_error_details(warn) for warn in warnings])
