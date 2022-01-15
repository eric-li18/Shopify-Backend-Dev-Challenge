from flask import Blueprint, request, send_from_directory
from sqlalchemy import func
from api.models import db, Item
from api import util
from api.handler import APIException, ResourceNotFoundException

bp = Blueprint("core", __name__)


@bp.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    util.validate_payload(data, "item_schema.json", "itemname", "price")

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
    rows = db.session.query(Item).order_by(Item.id)

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


@bp.route("/items/export", methods=["GET"])
def export_csv():
    columns = Item.__table__.columns.keys()
    rows = (
        db.session.query(Item)
        .with_entities(
            func.CONCAT_WS(
                ",", Item.id, Item.itemname, Item.price, Item.quantity, Item.description
            )
        )
        .order_by(Item.id)
    )

    path = "/app/export.csv"
    with open(path, "w+") as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        for item in rows:
            writer.writerow(",".join(item))
    return send_from_directory("", path)
