import os
from flask import json
from jsonschema import validate
from typing import Tuple
from api.handler import InvalidRequestException


def response(data: dict, status=200) -> Tuple[dict, int, dict]:
    return (json.dumps(data), status, {"content-type": "application/json"})


def validate_payload(data: dict, filename: str, *args) -> None:
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
    path = os.path.dirname(__file__)
    path = os.path.join(path, f"schemas/{filename}")
    with open(path, "r") as file:
        schema = json.load(file)
    return schema


def object_to_dict(obj: object) -> dict:
    obj_dict = vars(obj)
    obj_dict.pop("_sa_instance_state", None)
    return obj_dict
