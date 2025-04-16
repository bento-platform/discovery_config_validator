import orjson
from bento_lib.discovery import DiscoveryConfig, load_discovery_config_from_dict
from bento_lib.logging.structured.configure import configure_structlog, configure_structlog_uvicorn
from bento_lib.logging.structured.fastapi import build_structlog_fastapi_middleware
from fastapi import FastAPI, File, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request as StarletteRequest
from structlog.stdlib import BoundLogger, get_logger
from typing import Annotated

from .config import config
from .types import ValidationResponse
from .utils import reduce_error_details, warning_to_reduced_error_details

SERVICE_NAME = "dcv_server"

app = FastAPI()

# Logging setup --------------------------------------------------------------------------------------------------------

app.middleware("http")(build_structlog_fastapi_middleware(SERVICE_NAME))

configure_structlog(json_logs=config.use_json_logs, log_level="info")
configure_structlog_uvicorn()

service_logger: BoundLogger = get_logger(SERVICE_NAME)

# ----------------------------------------------------------------------------------------------------------------------


@app.exception_handler(StarletteHTTPException)
async def handle_404_or_serve_client(request: StarletteRequest, exc: StarletteHTTPException):
    # If the server is configured to serve the client, we want to serve the client for all non-API 404s, to allow the
    # front-end framework to handle paths as needed.
    if config.serve_client and exc.status_code == status.HTTP_404_NOT_FOUND and not request.url.path.startswith("/api"):
        return FileResponse(config.client_path / "index.html", media_type="text/html")
    return JSONResponse({"message": exc.detail}, status_code=exc.status_code)


@app.post("/api/v1/validate")
async def validate_config(file: Annotated[bytes, File()]) -> ValidationResponse:
    logger = service_logger.bind(action="validate_config", n_bytes=len(file))

    try:
        data = orjson.loads(file)
    except orjson.JSONDecodeError:
        logger.error("JSON decode error")
        return ValidationResponse(errors=[{"msg": "JSON decode error"}])

    discovery_config: DiscoveryConfig
    try:
        discovery_config, warnings = load_discovery_config_from_dict(data)
        logger = logger.bind(n_warnings=len(warnings))
    except ValidationError as e:
        e: ValidationError
        logger.error("validation failed", n_errors=e.error_count())
        return ValidationResponse(errors=[reduce_error_details(err) for err in e.errors()])

    logger.info("validation succeeded")

    return ValidationResponse(
        config=discovery_config, warnings=[warning_to_reduced_error_details(warn) for warn in warnings]
    )


@app.get("/api/v1/schema.json")
async def discovery_config_schema():
    return DiscoveryConfig.model_json_schema()


if config.serve_client:
    # If the server is configured to serve the client as well (the dist folder from the output of `npm build` or similar
    # in dcv_client, by default), we mount a static file service using the configured client path:
    app.mount("/", StaticFiles(directory=config.client_path, html=True))
