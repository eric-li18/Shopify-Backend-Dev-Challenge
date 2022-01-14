import os
from flask import json
from jsonschema import validate
from typing import Tuple
import sqlalchemy
from api.handler import InvalidRequestException


def response(data: dict, status=200) -> Tuple[dict, int, dict]:
    """Constructs common response structure in JSON format."""
    return (json.dumps(data), status, {"content-type": "application/json"})


def validate_payload(data: dict, filename: str, *args) -> None:
    """
    Applies the schema at 'filename' to  payload 'data' and
    checks for required arguments 'args'.
    """
    schema = get_schema(filename)
    validate(data, schema)

    if not data:
        raise InvalidRequestException("Missing request payload.")

    for key in args:
        if not data.get(key):
            raise InvalidRequestException(f"Missing '{key}' key in request.")


def get_schema(filename: str) -> dict:
    """Retrieves the schema for the given file."""
    if not filename:
        return None
    path = os.path.join(os.path.dirname(__file__), f"schemas/{filename}")
    with open(path, "r") as file:
        schema = json.load(file)
    return schema


def object_to_dict(obj: sqlalchemy.Model) -> dict:
    """Converts a given sqlalchemy.Model object into a dictionary."""
    obj_dict = vars(obj)
    obj_dict.pop("_sa_instance_state", None)
    return obj_dict
