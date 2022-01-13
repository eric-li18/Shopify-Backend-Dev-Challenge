from api import create_app
from api.models import db


app = create_app()
app.app_context().push()
db.drop_all()
db.create_all()