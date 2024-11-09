from database.models import Discount

def get_discount_from_code(discount_code):
    return Discount.query.filter_by(discount_code=discount_code).first()

def create_discount(name, discount_code, type, amount):
    return Discount(name=name, discount_code=discount_code, type=type, amount=amount)
