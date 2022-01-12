from . import db


class Item(db.Model):
    """Item Table"""

    id = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, default=0)

    def __init__(self, itemname):
        self.itemname = itemname

    def __repr__(self):
        return f"Item({self.id},{self.itemname},{self.quantity})"
