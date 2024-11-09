from app import app
from app.routes.helpers import privileged_route
from flask import request, render_template, redirect, url_for, flash

from app import app, db, bcrypt, loginmanager
from app.forms.createacc_form import createemp, updateemp, createcust, updatecust
from database.models import Employee, Customer, Orders
from app.forms.login_form import login, forget, reset

from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func, literal_column

# def query_count(query):
#     ONE = literal_column("1")
#     counter = query.statement.with_only_columns([func.count(ONE)])
#     counter = counter.order_by(None)
#     return query.session.execute(counter).scalar()

@app.route("/dashboard")
@login_required
def dash():
    # if not current_user.is_authenticated:
        # loginmanager.login_message = "Please login to access this page"
        # loginmanager.login_message_category = "warning"
    count = 0
    count2 = 0
    count3 = 0
    orders = Orders.query.filter_by(email=current_user.email)
    for order in orders:
        count += 1
        if order.status == "Dispatched":
            count2 += 1
        if order.status == "Delivered":
            count3 += 1
    return render_template('accounts/cust/dashboard/custdash.html', name=current_user.name, count=count, count2=count2, count3=count3)

@app.route("/admin")
@privileged_route("admin")
def admin():
    countcust = 0
    countemp = 0
    positions = [0,0,0,0,0]
    for i in Employee.query.all():
        if i.position == "Full-time":
            positions[0] += 1
        elif i.position == "Part-time":
            positions[1] += 1
        elif i.position == "Intern":
            positions[2] += 1
        elif i.position == "Admin":
            positions[3] += 1
        else:
            positions[4] += 1
        countemp += 1
    for i in Customer.query.all():
        countcust += 1
    total = countemp + countcust
    return render_template('admindash.html', current_user=current_user, countemp=countemp, countcust=countcust, total=total, positions=positions)

@app.route("/employee")
@privileged_route("emp")
def employee():
    countcust = 0
    countemp = 0
    positions = [0,0,0,0,0]
    for i in Employee.query.all():
        if i.position == "Full-time":
            positions[0] += 1
        elif i.position == "Part-time":
            positions[1] += 1
        elif i.position == "Intern":
            positions[2] += 1
        elif i.position == "Admin":
            positions[3] += 1
        else:
            positions[4] += 1
        countemp += 1
    for i in Customer.query.all():
        countcust += 1
    total = countemp + countcust
    return render_template('admindash.html', current_user=current_user, countemp=countemp, countcust=countcust, total=total, positions=positions)
