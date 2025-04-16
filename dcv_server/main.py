import orjson
from bento_lib.discovery import DiscoveryConfig, load_discovery_config_from_dict
from fastapi import FastAPI, File, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Annotated

from .types import ValidationResponse
from .utils import reduce_error_details, warning_to_reduced_error_details

app = FastAPI()


def serve_client():
    # TODO
    pass


config_serve_client = True


if config_serve_client:
    app.get("/index.html")(serve_client)


@app.exception_handler(StarletteHTTPException)
async def handle_404_or_serve_client(_request, exc: StarletteHTTPException):
    # TODO
    if config_serve_client and exc.status_code == status.HTTP_404_NOT_FOUND:
        serve_client()
    return JSONResponse({"message": exc.detail}, status_code=exc.status_code)


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


@app.get("/api/v1/schema.json")
async def discovery_config_schema():
    return DiscoveryConfig.model_json_schema()
