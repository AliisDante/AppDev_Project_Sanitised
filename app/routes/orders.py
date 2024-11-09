from flask import render_template, request, redirect, url_for, flash, abort
from database.models import Orders, OrderedItems, Products, Discount
from app import app, db, loginmanager
from datetime import datetime, timedelta, date
import hashlib
# from app.routes.gmail import gmail_authenticate, send_message
from app.email import send_message
from database import discounts
from app.routes.helpers import user_is_authenticated, get_user_permission_level_from_token

def authorised():
    if user_is_authenticated():
        privillaged_level = get_user_permission_level_from_token()
        if privillaged_level in ['admin', 'emp']:
            return True
        else:
            return False

    else:
        return False

@app.route("/orders", methods=['GET'])
def orders_dashboard():
    
    if authorised():
        # To clear DB
        # Orders.query.delete()
        # OrderedItems.query.delete()
        # db.session.commit()

        orders = Orders.query.all()
        products = Products.query.all()
        discounts = Discount.query.all()

        deliver = {}

        summaryCount = {
            'Production': 0,
            'Pending': 0,
            'Dispatched': 0,
            'Delivered': 0,
        }

        for order in orders:

            now = datetime.now()

            delivery_date = order.date + timedelta(days=10)
            delivery_string = delivery_date.strftime("%d/%m/%Y")

            time_diff = (delivery_date - now).days

            deliver[order.id] = [time_diff, delivery_string]

            summaryCount[order.status] += 1


        return render_template('orders/orders.html', orders=orders, products=products, discounts=discounts ,deliver=deliver, summaryCount=summaryCount)

    else:
        if user_is_authenticated():
            flash('You Are Not Authorised to View the Employee Portal', 'danger')
            return abort(403)
        else:
            return app.login_manager.unauthorized()
            

@app.route('/orders/create', methods=['POST'])
def create_order():

    if authorised():

        form = request.form

        now = datetime.now()

        email = form['email']
        discount_code = form['discount']

        order =  Orders(
            name = form['cname'],
            country = form['country'],
            contactCode = form['cCode'],
            contactNum = form['cnumber'],
            address = form['address'],
            email = email,
            notes = form['notes'],
            status = form['status'],
            date = now,
            customer_platform = 'Physical Store',
        )

        db.session.add(order)
        db.session.commit()

        orderid = order.id

        track = hashlib.md5((str(orderid)+ '!salt!').encode('utf-8')).hexdigest()
        Orders.query.filter_by(id=orderid).update(dict(trackingID=track))
        db.session.commit()

        order_value = 0
        product = None

        for key in form:
            if key.startswith('items'):
                order_item = form[key]
                product = Products.query.get(order_item)
                order_discount = product.discount

            if key.startswith('quantity'):
                order_quantity = form[key]
                new_stock_count = product.quantity - int(order_quantity)
                Products.query.filter_by(id=order_item).update(dict(quantity=new_stock_count))
                order_value += (product.price * (1 - (order_discount / 100))) * float(order_quantity)

            if key.startswith('requests'):
                order_requests = form[key]

                item = OrderedItems(
                    order_id = orderid,
                    item = order_item,
                    quantity = order_quantity,
                    requests = order_requests,
                    discount = order_discount,
                )

                db.session.add(item)
                db.session.commit()

        if order_value < 500:
            shipping_fee = 15
        else:
            shipping_fee = 0

        discount_amount = 0

        if discount_code == "" or discount_code == None:
            discount_amount = 0
            shipping_fee = 0
        else:
            discount = discounts.get_discount_from_code(discount_code)

            if discount is not None:
                if discount.type == "percentage":
                    subtotal = order_value + shipping_fee
                    discount_amount = subtotal * (discount.amount / 100)
                else:
                    discount_amount = discount.amount
                

        Orders.query.filter_by(id=orderid).update(dict(shipping_fee=shipping_fee))
        Orders.query.filter_by(id=orderid).update(dict(discount_code=discount_code))
        Orders.query.filter_by(id=orderid).update(dict(discount_amount=discount_amount))

        db.session.commit()
        db.session.close()

        # get the Gmail API service
        # service = gmail_authenticate()

        theOrder = Orders.query.get(orderid)
        prices = {}
        name_mapping = {}
        subtotal = 0
        order_created = theOrder.date.strftime("%d/%m/%Y %H:%M:%S")
        heading = "Thank you for your purchase!"

        for item in theOrder.items:
            product = Products.query.get(item.item)

            if product is not None:
                prices[item.item] = product.price * (1- (item.discount / 100))

                subtotal += prices[item.item] * item.quantity

                name_mapping[item.item] = product.name

        send_message(email, f"Odlanahor - Order Information", render_template("orders/order_mail.html", heading=heading, order=theOrder, prices=prices, name_mapping=name_mapping, subtotal=subtotal, order_created=order_created))

        return redirect(url_for('success_page', act='Created')) 
    
    else:
        if user_is_authenticated():
            flash('You Are Not Authorised to View the Employee Portal', 'danger')
            return abort(403)
        else:
            return app.login_manager.unauthorized()


@app.route('/orders/delete/<int:orderid>', methods=['POST'])
def delete_order(orderid):

    if authorised():

        exists = Orders.query.get(orderid) is not None

        if exists:

            order = Orders.query.get(orderid)

        for item in order.items:
            product = Products.query.get(item.item)
            new_stock_count = product.quantity + item.quantity
            Products.query.filter_by(id=item.item).update(dict(quantity=new_stock_count))

            db.session.delete(order)
            db.session.commit()

        db.session.close()

        return redirect(url_for('success_page', act='Deleted')) 
    
    else:
        if user_is_authenticated():
            flash('You Are Not Authorised to View the Employee Portal', 'danger')
            return abort(403)
        else:
            return app.login_manager.unauthorized()


@app.route('/orders/view/<int:orderid>', methods=['GET'])
def view_order(orderid):

    if authorised():

        order = Orders.query.get(orderid)

        order_created = order.date.strftime("%d/%m/%Y %H:%M:%S")

        prices = {}
        name_mapping = {}
        subtotal = 0

        for item in order.items:
            product = Products.query.get(item.item)

            if product is not None:

                prices[item.item] = product.price * (1- (item.discount / 100))

                subtotal += prices[item.item] * item.quantity

            name_mapping[item.item] = product.name

        if order.discount_amount == None:
            order.discount_amount = 0
    

        return render_template(
            'orders/view.html', 
            order=order, 
            order_created=order_created, 
            prices=prices, 
            subtotal=subtotal,
            name_mapping=name_mapping,
        )
        
    else:
        if user_is_authenticated():
            flash('You Are Not Authorised to View the Employee Portal', 'danger')
            return abort(403)
        else:
            return app.login_manager.unauthorized()

@app.route('/orders/update/<int:orderid>', methods=['POST'])
def update_order(orderid):

    if authorised():

        form = request.form

        exists = Orders.query.get(orderid) is not None

        email = form[f'email{orderid}']
        discount_code = form[f'discount{orderid}']

        if exists:

            order = Orders.query.get(orderid)

            order.name = form[f'cname{orderid}']
            order.country = form[f'country{orderid}']
            order.contactCode = form[f'cCode{orderid}']
            order.contactNum = form[f'cnumber{orderid}']
            order.address = form[f'address{orderid}']
            order.email = form[f'email{orderid}']
            order.notes = form[f'notes{orderid}']
            order.status = form[f'status{orderid}']

            db.session.commit()

            item_count = 0
            order_value = 0
            product = None

            for key in form:
                if key.startswith('items'):
                    item_count += 1
                    order_item = form[key]
                    product = Products.query.get(order_item)
                    order_discount = product.discount

                if key.startswith('quantity'):
                    order_quantity = form[key]
                    current_quan = int(order_quantity)

                    row = int(key.split("_")[1])
                    for i, item in enumerate(order.items):
                        if item.item == order_item and i+1 == row:
                            current_quan = item.quantity

                    new_stock_count = product.quantity + (current_quan - int(order_quantity))
                    Products.query.filter_by(id=order_item).update(dict(quantity=new_stock_count))
                    order_value += (product.price * (1 - (order_discount / 100))) * float(order_quantity)

                if key.startswith('requests'):
                    order_requests = form[key]

                    order.items[item_count-1].item = order_item
                    order.items[item_count-1].quantity = order_quantity
                    order.items[item_count-1].requests = order_requests
                    order.items[item_count-1].discount = order_discount

                    db.session.commit()

        if order_value < 500:
            shipping_fee = 15
        else:
            shipping_fee = 0

        discount_amount = 0

        if discount_code == "" or discount_code == None:
            discount_amount = 0
            shipping_fee = 0
        else:
            discount = discounts.get_discount_from_code(discount_code)

            if discount is not None:
                if discount.type == "percentage":
                    subtotal = order_value + shipping_fee
                    discount_amount = subtotal * (discount.amount / 100)
                else:
                    discount_amount = discount.amount


        Orders.query.filter_by(id=orderid).update(dict(shipping_fee=shipping_fee))
        Orders.query.filter_by(id=orderid).update(dict(discount_code=discount_code))
        Orders.query.filter_by(id=orderid).update(dict(discount_amount=discount_amount))


        db.session.commit()

        theOrder = Orders.query.get(orderid)
        prices = {}
        name_mapping = {}
        subtotal = 0
        order_created = theOrder.date.strftime("%d/%m/%Y %H:%M:%S")
        heading = "There was a change in your order"

    for item in theOrder.items:
        product = Products.query.get(item.item)

        if product is not None:

            prices[item.item] = product.price * (1- (item.discount / 100))

            subtotal += prices[item.item] * item.quantity

            name_mapping[item.item] = product.name

        send_message(email, f"Odlanahor - Order Information", render_template("orders/order_mail.html", heading=heading, order=theOrder, prices=prices, name_mapping=name_mapping, subtotal=subtotal, order_created=order_created))

        db.session.close()

        return redirect(url_for('success_page', act='Updated')) 

    else:
        if user_is_authenticated():
            flash('You Are Not Authorised to View the Employee Portal', 'danger')
            return abort(403)
        else:
            return app.login_manager.unauthorized()


@app.route('/order/success/<string:act>', methods=['GET'])
def success_page(act):

    if authorised():
        return render_template('/orders/orderSuccess.html', act=act), {'Refresh': '3; url=/orders'}
    else:
        if user_is_authenticated():
            flash('You Are Not Authorised to View the Employee Portal', 'danger')
            return abort(403)
        else:
            return app.login_manager.unauthorized()


@app.route('/track', methods=['GET', 'POST'])
def track_page():

    if request.method == 'POST':

        form = request.form
        trackID = form['trackID']
        now = datetime.now()

        try:
            orders = Orders.query.filter(Orders.trackingID == trackID)
            order = orders[0]
        except:
            return render_template('/orders/trackError.html')
        else:

            if order.status == 'Pending':
                delivery_date = now + timedelta(days=10)
            elif order.status == 'Production':
                delivery_date = now + timedelta(days=8)
            elif order.status == 'Dispatched':
                delivery_date = now + timedelta(days=1)
            else:
                delivery_date = now + timedelta(days=0)

            deliver = delivery_date.strftime("%d/%m/%Y")

            return render_template('/orders/tracking.html', order=order, deliver=deliver)

    return render_template('/orders/track.html')


# Data Generation For Statistics
# @app.route('/dummyOrders', methods=['GET'])
# def dummy():

#     # Change this
#     now = datetime.strptime('1Dec2022', '%d%b%Y')
#     order_item = '3'
#     order_quantity = 1
#     status = 'Delivered'

#     order_requests = ''
#     order_discount = 0

#     email = 'a@a'
#     discount_code = ''

#     order =  Orders(
#         name = 'a',
#         country = 'Singapore',
#         contactCode = '+65',
#         contactNum = '87654321',
#         address = 'a',
#         email = email,
#         notes = '',
#         status = status,
#         date = now,
#         customer_platform = 'Windows',
#     )

#     db.session.add(order)
#     db.session.commit()

#     orderid = order.id

#     track = hashlib.md5((str(orderid)+ '!salt!').encode('utf-8')).hexdigest()
#     Orders.query.filter_by(id=orderid).update(dict(trackingID=track))
#     db.session.commit()

#     item = OrderedItems(
#         order_id = orderid,
#         item = order_item,
#         quantity = order_quantity,
#         requests = order_requests,
#         discount = order_discount,
#     )

#     db.session.add(item)
#     db.session.commit()

#     shipping_fee = 0
#     discount_amount = 0

#     Orders.query.filter_by(id=orderid).update(dict(shipping_fee=shipping_fee))
#     Orders.query.filter_by(id=orderid).update(dict(discount_code=discount_code))
#     Orders.query.filter_by(id=orderid).update(dict(discount_amount=discount_amount))

#     db.session.commit()
#     db.session.close()

#     return redirect(url_for('success_page', act='Created')) 