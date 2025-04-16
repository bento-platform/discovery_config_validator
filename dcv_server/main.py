import orjson
from bento_lib.discovery import DiscoveryConfig, load_discovery_config_from_dict
from fastapi import FastAPI, File, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request as StarletteRequest
from typing import Annotated

from .config import config
from .types import ValidationResponse
from .utils import reduce_error_details, warning_to_reduced_error_details

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def handle_404_or_serve_client(request: StarletteRequest, exc: StarletteHTTPException):
    # If the server is configured to serve the client, we want to serve the client for all non-API 404s, to allow the
    # front-end framework to handle paths as needed.
    if config.serve_client and exc.status_code == status.HTTP_404_NOT_FOUND and not request.url.path.startswith("/api"):
        return FileResponse(config.client_path / "index.html", media_type="text/html")
    return JSONResponse({"message": exc.detail}, status_code=exc.status_code)


@app.post("/api/v1/validate")
async def validate_config(file: Annotated[bytes, File()]) -> ValidationResponse:
    try:
        data = orjson.loads(file)
    except orjson.JSONDecodeError:
        return ValidationResponse(errors=[{"msg": "JSON decode error"}])

    discovery_config: DiscoveryConfig
    try:
        discovery_config, warnings = load_discovery_config_from_dict(data)
    except ValidationError as e:
        e: ValidationError
        return ValidationResponse(errors=[reduce_error_details(err) for err in e.errors()])

    return ValidationResponse(
        config=discovery_config, warnings=[warning_to_reduced_error_details(warn) for warn in warnings]
    )


@app.get("/api/v1/schema.json")
async def discovery_config_schema():
    return DiscoveryConfig.model_json_schema()


if config.serve_client:
    app.mount("/", StaticFiles(directory=config.client_path, html=True))
