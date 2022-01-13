from flask import json
from sqlalchemy.engine import Row
from api.handler import InvalidRequestException


def response(data, status=200):
    return (json.dumps(data), status, {"content-type": "application/json"})


def validate_payload(data, *args):
    if not data:
        raise InvalidRequestException("Missing request payload.")

    for key in args:
        if not data.get(key):
            raise InvalidRequestException(f"Missing '{key}' key in request.")


def object_to_dict(row: Row) -> dict:
    result = vars(list(row._asdict().values())[0])
    result.pop("_sa_instance_state", None)
    return result
