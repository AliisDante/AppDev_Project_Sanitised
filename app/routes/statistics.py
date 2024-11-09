from flask import render_template, flash, abort 
from database.models import Orders, Products
from app import app
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
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

@app.route("/statistics", methods=['GET'])
def statistics_dashboard():

    if authorised():

        orders = Orders.query.all()

        dataMonth = {
            'Date': [],
        }
        ordersByMonth = {}
        sortedOrdersByMonth = {}
        prodsByCat = {}
        channel_count = {}
        line_data = []
        ring_data = []
        total_orders = 0
        total_revenue = 0

        now = datetime.now()
        endDate = now + relativedelta(months=+1)

        for order in reversed(orders):

            month = order.date.strftime("%b-%Y")

            if month in ordersByMonth and len(ordersByMonth) <= 8:
                ordersByMonth[month] += 1
            elif len(ordersByMonth) <= 8:
                ordersByMonth[month] = 1
                dataMonth["Date"].append(month)

            total_orders += 1

            if order.customer_platform in channel_count:
                channel_count[order.customer_platform] += 1
            else:
                channel_count[order.customer_platform] = 1

            for item in order.items:

                product = Products.query.get(item.item)

                if product is not None:
                    cat = product.type

                    if cat == 'H':
                        cat = 'Home Office'
                    elif cat == 'D':
                        cat = 'Dining'
                    elif cat == 'B':
                        cat = 'Bedding'
                    elif cat == 'L':
                        cat = 'Living'
                    else:
                        cat = 'Others'

                    if cat in prodsByCat:
                        prodsByCat[cat] += item.quantity
                    else:
                        prodsByCat[cat] = item.quantity

                    item_price = product.price * (1- (item.discount / 100))
                    total_revenue += item_price * item.quantity
        
            if order.discount_amount is not None:
                total_revenue -= order.discount_amount

        try:
            df = pd.DataFrame(dataMonth)
            df = df.set_index("Date")
            df.index = pd.to_datetime(df.index)
            df = df.sort_values(by='Date')

            date_range = pd.date_range(
                start=df.index[0], end=endDate, freq='M'
            ).to_period('m')
            
        except:
            pass
        else:

            for month in date_range:

                month = month.strftime("%b-%Y")

                if month not in ordersByMonth:
                    ordersByMonth[month] = 0

                sortedOrdersByMonth[month] = ordersByMonth[month]

            for month in sortedOrdersByMonth:

                if len(line_data) <= 8:
                    point = (month, sortedOrdersByMonth[month])
                    line_data.append(point) 


        for cat in prodsByCat:
            point = (cat, prodsByCat[cat])
            ring_data.append(point)

        
        if channel_count:
            top_channel = max(channel_count, key = lambda k: channel_count[k])
        else:
            top_channel = 'None'

        line_labels = [row[0] for row in line_data]
        line_values = [row[1] for row in line_data]

        ring_labels = [row[0] for row in ring_data]
        ring_values = [row[1] for row in ring_data]

        return render_template(
            'statistics/statistics.html', 
            total_orders=total_orders, 
            total_revenue=round(total_revenue),
            prodsByCat=prodsByCat,
            top_channel=top_channel,
            line_labels=line_labels, 
            line_values=line_values, 
            ring_labels=ring_labels,
            ring_values=ring_values,
        )

    else:
        if user_is_authenticated():
            flash('You Are Not Authorised to View the Employee Portal', 'danger')
            return abort(403)
        else:
            return app.login_manager.unauthorized()