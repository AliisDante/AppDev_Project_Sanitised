from flask import request, redirect, url_for, render_template, flash

from app import app
from app.routes.helpers import get_working_cart, update_cart, get_cart_value, get_shipping_fee, build_cart_key, disassemble_cart_key
from database import products

@app.route("/cart")
def view_cart():
    cart = get_working_cart()
    cart_products_objects = {}
    for cart_key, product_dictionary in cart.items():
        product_id, colour = disassemble_cart_key(cart_key)
        cart_products_objects[product_id] = products.get_product(product_id)
    cart_value = get_cart_value()
    shipping_fee = get_shipping_fee()
    subtotal = cart_value + shipping_fee
    tax = subtotal * 0.08
    total = subtotal + tax

    return render_template("cart/cart.html", cart=cart, cart_value=cart_value, shipping_fee=shipping_fee ,subtotal=subtotal, tax=tax, total=total, cart_products_objects=cart_products_objects, max_quantity_allowed=10)

@app.route("/cart/<product_id>/update", methods=["POST"])
def change_product_quantity(product_id):
    new_quantity = request.form.get("new-quantity", type=int)
    colour = request.form.get("colour")
    cart = get_working_cart()
    cart_key = build_cart_key(product_id, colour)
    product_obj = products.get_product(product_id)
    product_name = cart[cart_key]["name"]
    if new_quantity > 10:
        flash("For bulk orders (>10 items), please contact us", "danger")
    elif product_obj.quantity >= new_quantity:
        if new_quantity == product_obj.quantity:
            flash(f"No more stock for {product_name} available", "warning")
        elif new_quantity == 10:
            flash("For bulk orders (>10 items), please contact us", "warning")
        cart[cart_key]["quantity"] = new_quantity
        update_cart()
    else:
        flash(f"Insufficient stock for {product_name}", "danger")

    return redirect(url_for("view_cart"))

@app.route("/cart/<product_id>/delete", methods=["POST"])
def remove_product_from_cart(product_id):
    cart = get_working_cart()
    colour = request.form.get("colour")
    cart_key = build_cart_key(product_id, colour)
    del cart[cart_key]
    update_cart()
    flash("Item successfully deleted", "success")
    return redirect(url_for("view_cart"))
