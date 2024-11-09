import mimetypes
import secrets

from flask import request, render_template, redirect, url_for, flash, session, make_response, abort
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from database.models import Products, ProductReviews, Contact_Us , Contact_Us_Type, Employee
from database import products
from app import app, db, loginmanager
from app.forms.product_review_form import PostForm
from app.forms.contact_us_form import ContactUs , Enquiry_type
from app.routes.helpers import get_working_cart, update_cart, get_user_permission_level_from_token, build_cart_key, disassemble_cart_key ,user_is_authenticated,privileged_route,get_user_id_from_token
from datetime import date, datetime
from app.email import send_message


# sfJcg_mr4R

@app.route("/newarrivals")
def newarrival():
    product = Products.query.all()
    reviews = ProductReviews.query.all()
    return render_template('products/2_NewArrivals/NewArrival.html', products=product,reviews=reviews)


@app.route('/collections')
def collection():
    return render_template('products/3_ProductCategories/Collection.html')


@app.route('/living')
def living():
    product = Products.query.all()
    reviews = ProductReviews.query.all()
    count = 0
    for i in product:
        if i.type == 'L':
            count += 1
    return render_template('products/3_ProductCategories/Product_Category_View.html', products=product, count=count,
                           collection_type='Living', category="L", reviews=reviews)


@app.route('/bedding')
def bedding():
    product = Products.query.all()
    reviews = ProductReviews.query.all()
    count = 0
    for i in product:
        if i.type == 'B':
            count += 1

    return render_template('products/3_ProductCategories/Product_Category_View.html', products=product, count=count,
                           collection_type='Bedding', category="B", reviews=reviews)


@app.route('/dining')
def dining():
    product = Products.query.all()
    reviews = ProductReviews.query.all()
    count = 0
    for i in product:
        if i.type == 'D':
            count += 1

    return render_template('products/3_ProductCategories/Product_Category_View.html', products=product, count=count,
                           collection_type='Dining', category="D", reviews=reviews)


@app.route('/homeOffice')
def homeOffice():
    product = Products.query.all()
    reviews = ProductReviews.query.all()
    count = 0
    for i in product:
        if i.type == 'H':
            count += 1

    return render_template('products/3_ProductCategories/Product_Category_View.html', products=product, count=count,
                           collection_type='Home Office', category="H", reviews=reviews)


@app.route('/productView/<int:id>')
def productView(id):
    # ProductReviews.query.delete()
    # db.session.commit()
    if user_is_authenticated():
        position = get_user_permission_level_from_token()
    else:
        position = 'customer'
    print(position)
    product = Products.query.get_or_404(id)
    reviews = ProductReviews.query.filter_by(product_id=id)
    quantity = product.quantity
    if quantity > 10:
        quantity = 10
    if quantity <= 0:
        quantity = 0

    counter = 0
    for i in reviews:
        counter += 1
    discount = product.discount
    discounted_price = discount_calculator(product)

    return render_template('products/productViewV2.html', product=product, reviews=reviews, counter=counter,
                           redirect_url=request.url, quantity=quantity, discount=discount,
                           discounted_price=discounted_price, position=position)


def discount_calculator(product):
    if product.discount == None:
        discount = 0
    else:
        discount = product.discount
    return product.price * (1 - float(discount) / 100)


@app.route('/review/<int:id>', methods=['GET', 'POST'])
def productReview(id):
    if not user_is_authenticated():
        loginmanager.login_message = 'Please Login to Post A Review'
        loginmanager.login_message_category = 'warning'
        return app.login_manager.unauthorized()
    print(current_user.email)
    print(current_user.name)
    form = PostForm(request.form)
    product = Products.query.get_or_404(id)
    if request.method == "POST":
        product_id = id
        name = product.name
        title = form.title.data
        content = form.content.data
        rating = form.rating.data
        user = current_user.name
        user_email = current_user.email
        date_of_post = date.today()
        print(user, date_of_post)
        review = ProductReviews(product_id=product_id, product_name=name, title=title, rating=rating, content=content,
                                user=user, date_of_post=date_of_post, email=user_email)
        print(product_id, name, title, content, rating)
        flash(f'You Review has been Posted Successfully', 'success')

        db.session.add(review)
        db.session.commit()
        return redirect(url_for('productView', id=product_id))

    return render_template('products/create_post.html', form=form, product=product, title='')


@app.route('/review/<int:product_id>/<int:id>/update', methods=['GET', 'POST'])
def updateReview(product_id, id):
    product = Products.query.get_or_404(product_id)
    if not user_is_authenticated():
        loginmanager.login_message = f'Please Login to Update Review for {product.name}'
        loginmanager.login_message_category = 'warning'
        return app.login_manager.unauthorized()
    reviews = ProductReviews.query.filter_by(product_id=product_id)

    form = PostForm(request.form)
    for key in reviews:
        if key.id == id:
            privileged_level = get_user_permission_level_from_token()
            if privileged_level not in ['admin', 'emp']:
                if key.email != current_user.email:
                    return abort(403)
            form.content.data = key.content
            form.title.data = key.title
            rating = key.rating

    if request.method == 'POST':
        for i in reviews:
            if i.id == id:
                i.title = request.form.get('title')
                i.content = request.form.get('content')
                i.rating = form.rating.data
                db.session.commit()
                flash('You Post Has been Updated', 'success')
                return redirect(url_for('productView', id=product_id))

    return render_template('products/create_post.html', form=form, product=product, title='Update Post', rating=rating)


@app.route('/review/<int:product_id>/<int:id>/delete', methods=['GET', 'POST'])
def deleteReview(product_id, id):
    reviews = ProductReviews.query.get(id)
    if not user_is_authenticated():
        loginmanager.login_message = f'Please Login to Delete Your Review'
        loginmanager.login_message_category = 'warning'
        return app.login_manager.unauthorized()

    privileged_level = get_user_permission_level_from_token()
    if privileged_level not in ['admin', 'emp']:
        if reviews.email != current_user.email:
            return abort(403)
    db.session.delete(reviews)
    db.session.commit()
    flash('You Post Has been Deleted', 'warning')
    return redirect(url_for('productView', id=product_id))


def Product_dictionary(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))


@app.route('/addtocart', methods=['POST'])
def AddToCart():
    if not user_is_authenticated():
        loginmanager.login_message = f'Please Login to Add Product To Cart'
        loginmanager.login_message_category = 'warning'
        return app.login_manager.unauthorized()

    if request.method == "POST":
        product_id = request.form.get('product_id')
        colour = request.form.get('selected_color')
        quantity = request.form.get('quantity', type=int)
        product = products.get_product(product_id)

        shopping_cart = get_working_cart()

        cart_key = build_cart_key(product_id, colour)
        if cart_key in shopping_cart:
            shopping_cart[cart_key]["quantity"] += quantity
        else:
            new_product_dictionary = {'name': product.name, 'price': product.price, 'color': colour,
                                      'quantity': quantity, "colour_selection": product.color}
            shopping_cart[cart_key] = new_product_dictionary

        flash(f'{product.name} has been added successfully', 'success')
        update_cart()

    else:
        flash('Something Went Wrong on Our Side! Please try again later', 'danger')

    redirect_url = request.form.get("redirect-url") or "/"
    return redirect(redirect_url)


@app.route('/test/carts')
def getCart():
    if 'ShoppingCart' not in session or len(session['ShoppingCart']) <= 0:
        flash('The Cart is Empty', 'danger')
        return redirect(url_for('collection'))

    subtotal = 0
    grandtotal = 0
    for key, product in session['ShoppingCart'].items():
        subtotal += float(product['price']) * int(product['quantity'])
        tax = ("%.2f" % (.06 * float(subtotal)))
        grandtotal = float("%.2f" % (1.06 * subtotal))
    return render_template('cart/cart_testing.html', tax=tax, grandtotal=grandtotal)


@app.route("/product/<int:id>/image")
def get_product_image(id):
    product = products.get_product(id)
    product_image = product.image
    product_filename = product.image_filename
    response = make_response(product_image)
    response.content_type, response.content_encoding = mimetypes.guess_type(product_filename)
    return response



@app.route('/contactUs', methods=['GET', 'POST'])
def contactus():
    # Contact_Us.query.delete()
    # db.session.commit()
    form = ContactUs(request.form)

    contact_us_type_ = Contact_Us_Type.query.all()

    if current_user.is_authenticated:
        name = current_user.name
        email = current_user.email
        phone_number = current_user.contact

        form.name.data = name
        form.email.data = email
        form.phone_number.data = str(phone_number)


    if request.method == "POST" and form.validate():
        # creating the ticket number
        # date_sent = str(datetime.today())
        ticket_number = secrets.token_hex(4)

        # Getting the messages that have been posted
        name = form.name.data
        email = form.email.data
        phone = form.phone_number.data
        type = request.form.get('type')
        message = form.message.data
        subject = form.subject.data
        date_ = date.today()
        status = 'OPEN'
        try:
            contactUS = Contact_Us(ticket_number = ticket_number ,name=name, email=email, phone_number=phone, type=type, subject=subject, message=message, date=date_, status=status)
            send_message(email, f"ODLANAHOR - Contact Us - Ref:{ticket_number}", render_template("products/6_Contact Us/contact_us_email.html", name=name, message=message,type=type, ticket_number=ticket_number))
        except:
            flash('An Unexpected Error has Occured. Please Try Again', category='danger')
        else:


            flash('Your message has been successfully received', category='success')

            db.session.add(contactUS)
            db.session.commit()

            return redirect(request.referrer)



    return render_template('products/6_Contact Us/contact_us.html', form=form, contact_us_type =contact_us_type_)

@app.route('/contactUs/type', methods=['POST','GET'])
def contact_us_type():
    if user_is_authenticated():
        privillaged_level = get_user_permission_level_from_token()
        if privillaged_level in ['admin', 'emp']:
            form = Enquiry_type(request.form)
            contactUsType = Contact_Us_Type.query.all()
            if request.method == "POST" and form.validate():
                type = form.enquiry_type_add.data

                contactUsType_db = Contact_Us_Type(type=type.title())

                db.session.add(contactUsType_db)
                db.session.commit()
                # flash(f'Contact Us type {type.title()} has been sucessfully added', 'success')
                return redirect(request.referrer)
            return render_template('products/6_Contact Us/AddContactUsType.html', form=form, contactUsType=contactUsType)

        else:
            flash('You Are Not Authorised to View the Employee Portal', 'danger')
            return abort(403)

    else:
        loginmanager.login_message = f'Please Login to Access the Employee Portal'
        loginmanager.login_message_category = 'warning'
        return app.login_manager.unauthorized()



@app.route('/contactUs/type/<int:id>/Delete')
def delete_contact_us_type(id):
    if user_is_authenticated():
        privillaged_level = get_user_permission_level_from_token()
        if privillaged_level in ['admin', 'emp']:
            type = Contact_Us_Type.query.get_or_404(id)
            db.session.delete(type)
            db.session.commit()
            return redirect(url_for('contact_us_type'))
        else:
            flash('You Are Not Authorised to View the Employee Portal', 'danger')
            return abort(403)

    else:
        loginmanager.login_message = f'Please Login to Access the Employee Portal'
        loginmanager.login_message_category = 'warning'
        return app.login_manager.unauthorized()



@app.route('/contactUs/ticket')
def contact_us_ticket_and_type():
    if user_is_authenticated():
        privillaged_level = get_user_permission_level_from_token()
        if privillaged_level in ['admin', 'emp']:
            return render_template('products/6_Contact Us/tickets_landing_screen.html')
        else:
            flash('You Are Not Authorised to View the Employee Portal', 'danger')
            return abort(403)

    else:
        loginmanager.login_message = f'Please Login to View Contact Us Tickets'
        loginmanager.login_message_category = 'warning'
        return app.login_manager.unauthorized()


@app.route('/contactUs/ticket/view')
def view_contact_us_ticket():
    # Contact_Us.query.delete()
    # db.session.commit()
    tickets = Contact_Us.query.all()
    if user_is_authenticated():
        privillaged_level = get_user_permission_level_from_token()
        if privillaged_level in ['admin', 'emp']:
            return render_template('products/6_Contact Us/View_ContactUs_Submissions.html', tickets=tickets)
        else:
            flash('You Are Not Authorised to View the Employee Portal', 'danger')
            return abort(403)
    else:
        loginmanager.login_message = f'Please Login to Access the Employee Portal'
        loginmanager.login_message_category = 'warning'
        return app.login_manager.unauthorized()

@app.route('/contactUs/ticket/<ticket_number>/reply', methods=['POST','GET'])
def contact_us_ticket_reply(ticket_number):
    ticket = Contact_Us.query.get_or_404(ticket_number)

    if user_is_authenticated():
        privillaged_level = get_user_permission_level_from_token()
        if privillaged_level in ['admin', 'emp']:
            employee_id = get_user_id_from_token()
            employee = Employee.query.get_or_404(employee_id)
            employee_name = employee.name

            if request.method =='POST':
                recipient_name = ticket.name
                recipient_email = ticket.email

                reply_subject = request.form.get('reply_subject')
                reply_msg = request.form.get('reply_message')
                type = ticket.type

                try:
                    send_message(recipient_email, f"ODLANAHOR - REPLY - Ref: {ticket_number}", render_template("products/6_Contact Us/reply_email_template.html", name=recipient_name, message=reply_msg,type=type, ticket_number=ticket_number, employee_name=employee_name))
                    ticket.status = 'CLOSED'
                    db.session.commit()
                except:
                    flash('An Unexpected Error has Occured','danger')
                else:
                    flash(f'Reply to Ticket Number ({ticket_number}) is Successful' ,'success')
                    return redirect(url_for('view_contact_us_ticket'))
            return render_template('products/6_Contact Us/reply_email.html', ticket=ticket, employee_name=employee_name)

        else:
            flash('You Are Not Authorised to Reply to the Customer\'s ticket', 'danger')
            return abort(403)

    else:
        loginmanager.login_message = f'Please Login to Access the Employee Portal'
        loginmanager.login_message_category = 'warning'
        return app.login_manager.unauthorized()

@app.route('/contactUs/ticket/<ticket_number>/Replied')
def contact_us_ticket_replied(ticket_number):
    if user_is_authenticated():
        privillaged_level = get_user_permission_level_from_token()
        if privillaged_level in ['admin', 'emp']:
            ticket = Contact_Us.query.get_or_404(ticket_number)
            db.session.delete(ticket)
            db.session.commit()
            return redirect(url_for('view_contact_us_ticket'))
        else:
            flash('You Are Not Authorised to Reply to the Customer\'s ticket', 'danger')
            return abort(403)

    else:
        loginmanager.login_message = f'Please Login to Delete Tickets'
        loginmanager.login_message_category = 'warning'
        return app.login_manager.unauthorized()
