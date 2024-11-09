import app
from app import db, loginmanager
from flask_login import UserMixin
from itsdangerous import TimedSerializer
from app.config import Config
import jwt
import datetime

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True, unique=False)
    type = db.Column(db.String(80), index=True, unique=False)
    quantity = db.Column(db.Integer, index=True, unique=False)
    restock_status = db.Column(db.String(80), index=True, unique=False)
    description = db.Column(db.String(300), index=True, unique=False)
    price = db.Column(db.Float, index=True, unique=False)
    sold = db.Column(db.Integer, index=True, unique=False)
    color = db.Column(db.String(80), index=True, unique=False)
    product_nature = db.Column(db.String(150), index=True , unique=False)
    picture_1 = db.Column(db.String(80), index=True, unique=False)
    # picture_1 = db.Column(db.LargeBinary)
    # picture_2 = db.Column(db.LargeBinary , nullable=True)
    # picture_3 = db.Column(db.LargeBinary , nullable=True)
    discount = db.Column(db.Float, index=True, unique=False)



class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.relationship('OrderedItems', backref='orders', lazy=True)
    name = db.Column(db.String(80), index=True, unique=False)
    country = db.Column(db.String(80), index=True, unique=False)
    contactCode = db.Column(db.String(10), index=True, unique=False)
    contactNum = db.Column(db.String(50), index=True, unique=False)
    address = db.Column(db.String(200), index=True, unique=False)
    email = db.Column(db.String(100), index=True, unique=False)
    notes = db.Column(db.String(300), index=True, unique=False)
    status = db.Column(db.String(20), index = True, unique = False)
    date = db.Column(db.DateTime(50), index = True, unique = False)
    trackingID = db.Column(db.String(50), index = True, unique = True, nullable = True)
    customer_platform = db.Column(db.String(256))
    shipping_fee = db.Column(db.Float)
    discount_code = db.Column(db.String(256))
    discount_amount = db.Column(db.Float)


class OrderedItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    item = db.Column(db.String(80), index=True, unique=False)
    quantity = db.Column(db.Integer, index=True, unique=False)
    requests = db.Column(db.String(300), index=True, unique=False)
    discount = db.Column(db.Float, index=True, unique=False, default=0)



class ProductReviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, index=True, unique=False)
    product_name = db.Column(db.String(100) ,index=True, unique=False)
    title = db.Column(db.String(100), index=True, unique=False)
    rating = db.Column(db.Integer, index=True, unique=False)
    content = db.Column(db.String, index=True, unique=False)
    user = db.Column(db.String(80), index=True, unique=False)
    email = db.Column(db.String(80), index=True, unique=False)
    date_of_post = db.Column(db.String(80), index=True, unique=False)


class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True, unique=False)
    gender = db.Column(db.String(80), index=True, unique=False)
    email = db.Column(db.String(80), index=True, unique=True)
    password = db.Column(db.String(80), index=True, unique=False)
    contact = db.Column(db.Integer, index=True, unique=False)
    position = db.Column(db.String(80), index=True, unique=False)

class Discount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    discount_code = db.Column(db.String(256))
    type = db.Column(db.String(256))
    amount = db.Column(db.Float)

class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True, unique=False)
    gender = db.Column(db.String(80), index=True, unique=False)
    email = db.Column(db.String(80), index=True, unique=True)
    password = db.Column(db.String(80), index=True, unique=False)
    contact = db.Column(db.Integer, index=True, unique=False)

    def get_reset_token(self, expires_sec=1800):
        reset_token = jwt.encode(
            payload=
            {
                "user_id": self.id,
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                       + datetime.timedelta(seconds=expires_sec)
            },
            key = app.app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return reset_token

    def verify_reset_token(token):
        try:
            userid = jwt.decode(token, key = app.app.config['SECRET_KEY'], leeway=datetime.timedelta(seconds=10), algorithms=['HS256', ])["user_id"]
        except:
            return None
        return Customer.query.filter_by(id=userid).first()


class Contact_Us(db.Model):
    ticket_number = db.Column(db.String(80), index=True, unique=False , primary_key=True)
    name = db.Column(db.String(80), index=True, unique=False)
    email = db.Column(db.String(100), index=True, unique=False)
    phone_number = db.Column(db.String(50), index=True, unique=False)
    type = db.Column(db.String(150), index=True, unique=False)
    subject = db.Column(db.String(80), index=True, unique=False)
    message = db.Column(db.String(500), index=True, unique=False)
    date = db.Column(db.String(80), index=True, unique=False)
    status = db.Column(db.String(80), index=True, unique=False)
class Contact_Us_Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), index=True, unique=True)
