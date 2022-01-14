from flask import Blueprint, request
from api.models import db, Item
from api import util
from api.handler import APIException, ResourceNotFoundException

bp = Blueprint("core", __name__)


@bp.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    util.validate_payload(data, "item_schema.json", "itemname", "price")

    """
    item_exists = (
        db.session.query(Item)
        .filter(Item.itemname == data.get("itemname"), Item.price == data.get("price"))
        .count()
    )
    db.session.commit()
    print(item_exists)

    if item_exists:
        return util.response({"error": "item exists"}, 400)
    """

    item = Item(**data)
    db.session.add(item)
    db.session.commit()
    return util.response({"message": "Item successfully created"}, 201)


@bp.route("/items/<item_id>", methods=["PATCH"])
def update_item(item_id):
    data = request.get_json()
    util.validate_payload(data, filename="item_schema.json")

    rows_updated = (
        db.session.query(Item)
        .filter(Item.id == item_id)
        .update(data, synchronize_session="fetch")
    )
    db.session.commit()

    if rows_updated < 1:
        raise ResourceNotFoundException(f"Item ID '{item_id}' does not exist")

    query_stmt = db.session.query(Item).filter(Item.id == item_id)
    result = db.session.execute(query_stmt).first()

    if not result:
        raise APIException()

    item = util.object_to_dict(result.Item)

    return util.response(item, 200)


@bp.route("/items", methods=["GET"])
def get_items():
    response = []
    rows = db.session.query(Item).order_by(Item.id).all()

    for item in rows:
        response.append(util.object_to_dict(item))

    return util.response(response, 200)


@bp.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    rows_deleted = (
        db.session.query(Item)
        .filter(Item.id == item_id)
        .delete(synchronize_session="fetch")
    )
    db.session.commit()

    if rows_deleted < 1:
        raise ResourceNotFoundException(f"Item ID '{item_id}' does not exist")

    return util.response({}, 204)