from flask import redirect, url_for, render_template, g

from app import app
from app.routes.helpers import user_is_authenticated, get_working_cart
from app.view_counter import add_view_count , ViewCounter
from app.routes import dashboard, inventory, orders, products, checkout, accounts, cart, statistics, gmail, chatbot
# @app.route("/")
# def index():
#     if user_is_authenticated():
#         return redirect(url_for("admin_dashboard"))
#     else:
#         return redirect(url_for("customer_dashboard"))

@app.before_request
def add_cart_item_count():
    cart_item_count = len(get_working_cart())
    g.cart_item_count = cart_item_count

@app.route('/')
def products():
    from database.models import Products, ProductReviews
    product = Products.query.all()
    reviews = ProductReviews.query.all()


    return render_template('products/1_ Home/homeV2.html' , products = product,  reviews = reviews )


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def access_denied(e):
    return render_template('403.html') , 403
