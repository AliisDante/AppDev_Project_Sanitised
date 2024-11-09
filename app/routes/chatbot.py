from flask import request, url_for
from flask_login import current_user, AnonymousUserMixin

from app import app
from database import products


@app.route("/chatbot/new_message", methods=["POST"])
def ask_chatbot():
    prompt = request.form.get("prompt").lower()
    return_list = []

    product = products.get_product_by_name_ilike(prompt)
    if prompt == "":
        return_list.append(f"Sorry, I do not understand your intention.<br><br>Please {generate_a_tag('/contactUs', 'contact us')} for further assistance.")
    elif prompt_matches(prompt, "all products"):
        for i in products.get_all_products():
            return_list.append(generate_product_string(i))
    elif prompt_matches(prompt, "info") or prompt_matches(prompt, "my info"):
        if isinstance(current_user, AnonymousUserMixin):
            return_list.append("You are not logged in")
        else:
            return_list.append(f"Your information<br>Name: {current_user.name}<br>Email: {current_user.email}<br>Contact Number: {current_user.contact}")
    elif prompt_matches(prompt, "login") or prompt_matches(prompt, "account"):
        return_list.append(f"Login to your account at this link: {generate_a_tag('/login', 'Login Page')}")
    elif prompt_matches(prompt, "contact us"):
        return_list.append(f"Contact us here: {generate_a_tag('/contactUs', 'Contact Us Page')}")
    elif prompt_matches(prompt, "hello"):
        return_list.append("Hello!")
    elif product:
        return_list.append(generate_product_string(product))
    else:
        return_list.append(f"Sorry, I do not understand your intention.<br><br>Please {generate_a_tag('/contactUs', 'contact us')} for further assistance.")
    return return_list


def generate_product_string(product):
    product_colours = product.color.split(",")
    return f"Found product {product.name}<br>Price: ${product.price}<br>Colour(s): {product.color}<br><br>Find out more about {generate_a_tag(url_for('productView', id=product.id), product.name)}<br><br>Or add to cart:<br><form action='/addtocart' method='post' class='mt-3'><input type='hidden' name='product_id' value='{product.id}'><input type='hidden' name='selected_color' value='{product_colours[0]}'><input type='hidden' name='quantity' value='1'><input type='hidden' name='redirect-url' value='/cart'><button type='submit' class='btn btn-primary'>Add to cart</button></form>"


def generate_a_tag(url, content):
    return f'<a href="{url}">{content}</a>'


def prompt_matches(prompt, match_string):
    return prompt == match_string
