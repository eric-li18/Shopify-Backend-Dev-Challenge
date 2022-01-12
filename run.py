from api import create_app
from api.models import db, Item
from api.models.Item import Item


app = create_app()
app.app_context().push()
db.create_all()
item = Item("test")
db.session.add(item)
db.session.commit()
print(Item.query.all())