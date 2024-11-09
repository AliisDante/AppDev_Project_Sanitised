from app import app
from database.models import Products

PRODUCT_IMAGES_DIRECTORY_PREFIX = "../app/static/products/imageStorage/"

products = Products.query.all()

def load_image_data(filename):
    filename = PRODUCT_IMAGES_DIRECTORY_PREFIX + filename
    with open(filename, "rb") as image_file:
        return image_file.read()

for i in products:
    if i.product_nature == "N":
        product_image_filename = f"NewArrival/{i.name}.jpg"
    elif i.product_nature == "P":
        product_image_filename = f"Promotional/{i.name}.jpg"
    elif i.type == "B":
        product_image_filename = f"Regular/Bedding/{i.name}.jpg"
    elif i.type == "D":
        product_image_filename = f"Regular/Dining/{i.name}.jpg"
    elif i.type == "H":
        product_image_filename = f"Regular/homeOffice/{i.name}.jpg"
    elif i.type == "L":
        product_image_filename = f"Regular/Living/{i.name}.jpg"

    product_image = load_image_data(product_image_filename)
    i.image = product_image
    i.image_filename = product_image_filename

db.session.commit()
