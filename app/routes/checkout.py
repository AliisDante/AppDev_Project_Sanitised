from functools import wraps
import json
import hashlib
import datetime

import httpagentparser
from flask import redirect, url_for, render_template, request, flash
from flask_login import current_user

from app import email
from app import app, db
from app.routes.helpers import get_working_cart, clear_cart, get_cart_value, get_shipping_fee, disassemble_cart_key
from database.models import Orders, OrderedItems
from database import products, discounts


def get_current_date():
    return datetime.datetime.today()


def generate_tracking_id(order_id):
    return hashlib.md5((str(order_id) + '!salt!').encode('utf-8')).hexdigest()


def get_user_platform(user_agent_string):
    user_agent = httpagentparser.detect(user_agent_string)
    if "dist" in user_agent:
        return user_agent["dist"]["name"]
    elif "os" in user_agent:
        return user_agent["os"]["name"]


def formify(route, get_view_function):
    def wrapper(post_view_function):
        @app.route(route, methods=["GET", "POST"])
        @wraps(post_view_function)
        def wrapped(*args, **kwargs):
            if request.method == "POST":
                return post_view_function(*args, **kwargs)
            else:
                return get_view_function(*args, **kwargs)

        return wrapped
    return wrapper


def checkout():
    cart = get_working_cart()
    if cart == {}:
        flash("No products in cart", "warning")
        return redirect(url_for("view_cart"))

    cart_value = get_cart_value()
    shipping_fee = get_shipping_fee()
    subtotal = cart_value + shipping_fee
    tax = subtotal * 0.08
    total = subtotal + tax

    current_user_name = current_user.name
    current_user_email = current_user.email
    current_user_contact_number = current_user.contact
    return render_template("checkout/checkout.html", cart_products=cart, cart_value=cart_value, shipping_fee=shipping_fee, subtotal=subtotal, tax=tax, total=total, current_user_name=current_user_name, current_user_email=current_user_email, current_user_contact_number=current_user_contact_number)


@formify("/checkout", checkout)
def confirm_checkout():
    delivery_name = request.form.get("delivery-name")
    delivery_email = request.form.get("delivery-email")
    delivery_country_code = request.form.get("delivery-country-code")
    delivery_contact_number = request.form.get("delivery-contact-number")
    delivery_country = request.form.get("delivery-country")
    delivery_postal_code = request.form.get("delivery-postal-code")
    delivery_address = request.form.get("delivery-address")

    payment_name = request.form.get("payment-name")
    payment_card_number = request.form.get("payment-card-number")
    payment_expiry_date_month = request.form.get("payment-expiry-date-month")
    payment_expiry_date_year = request.form.get("payment-expiry-date-year")
    payment_cvv = request.form.get("payment-cvv")

    user_agent_string = request.user_agent.string
    user_platform = get_user_platform(user_agent_string)

    discount_code = request.form.get("discount-code")
    if discount_code == "":
        discount_amount = 0
        shipping_fee = 0
    else:
        discount = discounts.get_discount_from_code(discount_code)
        if discount.type == "percentage":
            cart_value = get_cart_value()
            shipping_fee = get_shipping_fee()
            subtotal = cart_value + shipping_fee
            discount_amount = subtotal * (discount.amount / 100)
        else:
            discount_amount = discount.amount

    if len(delivery_postal_code) != 6:
        flash("Postal Code is invalid", "danger")
        return redirect(url_for("confirm_checkout"))

    if len(payment_expiry_date_month) != 2:
        flash("Expiry date month must have 2 digits", "danger")
        return redirect(url_for("confirm_checkout"))

    if len(payment_expiry_date_year) != 2:
        flash("Expiry date year must have 2 digits", "danger")
        return redirect(url_for("confirm_checkout"))

    if len(payment_card_number) != 16:
        flash("Card number must have 16 digits", "danger")
        return redirect(url_for("confirm_checkout"))

    if len(payment_cvv) not in [3, 4]:
        flash("Card CVV must 3 or 4 digits", "danger")
        return redirect(url_for("confirm_checkout"))

    cart = get_working_cart()

    new_order = Orders(name=delivery_name,
                       country=delivery_country,
                       contactCode=delivery_country_code,
                       contactNum=delivery_contact_number,
                       address=delivery_address,
                       email=delivery_email,
                       customer_platform=user_platform,
                       date=get_current_date(),
                       status="Pending",
                       discount_amount=discount_amount,
                       shipping_fee=shipping_fee)

    db.session.add(new_order)
    db.session.commit()

    new_order_id = new_order.id
    new_tracking_id = generate_tracking_id(new_order_id)
    new_order.trackingID = new_tracking_id

    for cart_key, product_dictionary in cart.items():
        product_id, colour = disassemble_cart_key(cart_key)
        product = products.get_product(product_id)
        quantity = product_dictionary["quantity"]
        db.session.add(OrderedItems(order_id=new_order_id, item=product_id, quantity=quantity, discount=product.discount))
        product.quantity -= quantity
        product.sold += quantity

    db.session.commit()

    email.send_message(delivery_email, f"Odlanahor - Order {new_tracking_id}", render_template("checkout/checkout_email.html", name=delivery_name, checkout_products=cart))

    clear_cart()

    return redirect(url_for("checkout_complete", tracking_id=new_tracking_id))


@app.route("/checkout/check_discount", methods=["POST"])
def check_discount():
    discount_code = request.form.get("discount-code")
    discount = discounts.get_discount_from_code(discount_code)

    if not discount:
        return json.dumps({"valid": False})

    return json.dumps({"valid": True, "name": discount.name, "type": discount.type, "amount": discount.amount})


@app.route("/checkout/complete")
def checkout_complete():
    tracking_id = request.args.get("tracking_id")
    hostname = request.host
    return render_template("checkout/complete.html", hostname=hostname, tracking_id=tracking_id)
