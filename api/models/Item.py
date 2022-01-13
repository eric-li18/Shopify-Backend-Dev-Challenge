from .db import db


class Item(db.Model):
    """Item Table"""

    id = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0)
    quantity = db.Column(db.Integer, default=0)
    description = db.Column(db.String(100))

    def __init__(self, itemname, price, quantity=0, description=None):
        self.itemname = itemname
        self.price = price
        self.quantity = quantity
        self.description = description

    def __repr__(self):
        return f"Item({self.id},{self.itemname},{self.price},{self.quantity},{self.description})"
