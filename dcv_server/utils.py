from pydantic_core import ErrorDetails
from .types import ReducedErrorDetails

__all__ = ["reduce_error_details", "warning_to_reduced_error_details"]


def reduce_error_details(v: ErrorDetails) -> ReducedErrorDetails:
    return {"loc": v["loc"], "msg": v["msg"]}


def warning_to_reduced_error_details(v: tuple[tuple[int | str, ...], str]) -> ReducedErrorDetails:
    return {"loc": v[0], "msg": v[1]}
