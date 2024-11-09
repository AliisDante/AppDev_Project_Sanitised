from app import app as flask_app
from app import db
from database.models import *

with flask_app.app_context():
    product_1 = Products(name="Sofa Set 1", type="B", color="Red", price=99.99)
    product_2 = Products(name="Chair Set 1", type="B", color="Red", price=9.99)

    db.session.add(product_1)
    db.session.add(product_2)

    db.session.commit()
