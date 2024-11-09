from app import db
from database.models import Products


def get_product_by_name(name):
    return Products.query.filter_by(name=name).first()


def get_product_by_name_ilike(name):
    return Products.query.filter(Products.name.ilike(f"%{name}%")).first()


def get_product(id):
    return Products.query.get(id)


def get_all_products():
    return Products.query.all()


def add_product_image(id, image_data, image_filename):
    product = get_product(id)
    product.image = image_data
    product.image_filename = image_filename
    db.session.commit()
