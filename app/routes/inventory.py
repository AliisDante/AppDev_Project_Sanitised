from flask import request, render_template, redirect, url_for, flash,abort
from app.routes.helpers import user_is_authenticated, get_user_permission_level_from_token
from app import app, db , loginmanager
from app.forms.inventory_form import FormProducts, Restock,UpdateProducts
from database.models import Products
import os
@app.route('/inventory')
def view_products():
    if user_is_authenticated():
        privileged_level = get_user_permission_level_from_token()
        if privileged_level in ['admin', 'emp']:
            products = Products.query.all()
            return render_template('inventory/view.html', products=products)
        else:
            flash('You Are Not Authorised to View the Employee Portal', 'danger')
            return abort(403)
    else:
        loginmanager.login_message_category = 'warning'
        return app.login_manager.unauthorized()



@app.route('/inventory/add', methods=["GET","POST"])
def add_products():
    if user_is_authenticated():
        privileged_level = get_user_permission_level_from_token()
        if privileged_level in ['admin', 'emp']:
            addproducts_form = FormProducts(request.form)
            if addproducts_form.validate() and request.method == "POST":
                picture_1 = save_image(request.files.get('picture_1'), request.files.get('picture_1').filename)
                product = Products(name=addproducts_form.name.data.title(), type=addproducts_form.type.data,
                                   quantity=addproducts_form.quantity.data, price=addproducts_form.price.data,
                                   restock_status="-", description=addproducts_form.description.data, sold=0,
                                   color=addproducts_form.color.data,
                                   product_nature=addproducts_form.product_nature.data,
                                   picture_1=picture_1.filename, discount=addproducts_form.discount.data)
                db.session.add(product)
                db.session.commit()
                db.session.close()
                flash(f"{addproducts_form.name.data.title()} has been successfully added to Inventory","danger")
                return redirect(url_for('view_products'))

            return render_template('inventory/add.html', form=addproducts_form)
        else:
            flash('You Are Not Authorised to View the Employee Portal', 'danger')
            return abort(403)
    else:
        loginmanager.login_message_category = 'warning'
        return app.login_manager.unauthorized()



@app.route('/inventory/delete')
def delete_products():
    if user_is_authenticated():
        privileged_level = get_user_permission_level_from_token()
        if privileged_level in ['admin', 'emp']:
            products = Products.query.all()
            return render_template('inventory/delete_product.html', products=products)
        else:
            flash('You Are Not Authorised to View the Employee Portal', 'danger')
            return abort(403)
    else:
        loginmanager.login_message_category = 'warning'
        return app.login_manager.unauthorized()

@app.route('/inventory/delete/<id>')
def p_delete(id):
    if user_is_authenticated():
        privileged_level = get_user_permission_level_from_token()
        if privileged_level in ['admin', 'emp']:
            p = Products.query.filter_by(id=id).first()
            picture_name = Products.query.get(id).picture_1
            if p:
                delete_image(picture_name)
                db.session.delete(p)
                db.session.commit()
                flash(f'{p.name} has been successfully deleted', 'danger')
            return redirect(url_for('delete_products'))
        else:
            flash('You Are Not Authorised to View the Employee Portal', 'danger')
            return abort(403)
    else:
        loginmanager.login_message_category = 'warning'
        return app.login_manager.unauthorized()


@app.route('/inventory/restock')
def restock():
    if user_is_authenticated():
        privileged_level = get_user_permission_level_from_token()
        if privileged_level in ['admin', 'emp']:
            products = Products.query.all()
            return render_template('inventory/restock.html', products=products)
        else:
            flash('You Are Not Authorised to View the Employee Portal', 'danger')
            return abort(403)
    else:
        loginmanager.login_message_category = 'warning'
        return app.login_manager.unauthorized()

@app.route('/inventory/restock/<id>',methods=["GET","POST"])
def restock_form(id):
    if user_is_authenticated():
        privileged_level = get_user_permission_level_from_token()
        if privileged_level in ['admin', 'emp']:
            restock_form = Restock(request.form)
            name = Products.query.get_or_404(id).name
            if restock_form.validate() and request.method == "POST":
                restock = restock_form.quantity.data
                product_restocked = Products.query.get_or_404(id)
                product_restocked.quantity += restock
                product_restocked.restock_status = "Waiting"
                db.session.commit()
                db.session.close()
                flash(f"A request has been sent to restock {name}", "danger")
                return redirect(url_for('restock'))

            return render_template('inventory/restock_form.html', form=restock_form, name=name)
        else:
            flash('You Are Not Authorised to View the Employee Portal', 'danger')
            return abort(403)
    else:
        loginmanager.login_message_category = 'warning'
        return app.login_manager.unauthorized()


@app.route('/inventory/restock/<id>/changed')
def restock_status_original(id):
    if user_is_authenticated():
        privileged_level = get_user_permission_level_from_token()
        if privileged_level in ['admin', 'emp']:
            Products.query.get_or_404(id).restock_status = "-"
            name = Products.query.get_or_404(id).name
            db.session.commit()
            db.session.close()
            flash(f"{name} has been succesfully restocked","success")
            return redirect(url_for('restock'))
        else:
            flash('You Are Not Authorised to View the Employee Portal', 'danger')
            return abort(403)
    else:
        loginmanager.login_message_category = 'warning'
        return app.login_manager.unauthorized()


@app.route('/inventory/update')
def update():
    if user_is_authenticated():
        privileged_level = get_user_permission_level_from_token()
        if privileged_level in ['admin', 'emp']:
            products = Products.query.all()
            return render_template('inventory/update.html', products=products)
        else:
            flash('You Are Not Authorised to View the Employee Portal', 'danger')
            return abort(403)
    else:
        loginmanager.login_message_category = 'warning'
        return app.login_manager.unauthorized()

@app.route('/inventory/update/<id>',methods=["GET","POST"])
def update_form(id):
    if user_is_authenticated():
        privileged_level = get_user_permission_level_from_token()
        if privileged_level in ['admin', 'emp']:
            update_form = UpdateProducts(request.form)
            product = Products.query.get_or_404(id)
            name = product.name
            y = product.description
            if update_form.validate() and request.method == "POST":
                if update_form.name.data != "" and product.name != update_form.name.data:
                    product.name = update_form.name.data.title()
                if update_form.type.data != "" and product.type != update_form.type.data:
                    product.type = update_form.type.data
                if update_form.color.data != "" and product.color != update_form.color.data:
                    product.color = update_form.color.data
                if update_form.price.data != "" and product.price != update_form.price.data:
                    product.price = update_form.price.data
                if update_form.product_nature.data != "" and product.product_nature != update_form.product_nature.data:
                    product.product_nature = update_form.product_nature.data
                if update_form.discount.data != "" and product.discount != update_form.discount.data:
                    product.discount = update_form.discount.data
                if product.description != update_form.description.data:
                    product.description = update_form.description.data
                if request.files.get("picture_1").filename != "" :
                    delete_image(product.picture_1)
                    new_picture_1 = save_image(request.files.get('picture_1'), request.files.get('picture_1').filename)
                    product.picture_1 = new_picture_1.filename
                x = update_form.description.data

                db.session.commit()
                db.session.close()
                flash(f"{y} has been succesfully updated to {x}", "danger")
                return redirect(url_for('update'))

            return render_template('inventory/update_form.html', form=update_form, product=product)

        else:
            flash('You Are Not Authorised to View the Employee Portal', 'danger')
            return abort(403)
    else:
        loginmanager.login_message_category = 'warning'
        return app.login_manager.unauthorized()

def save_image(image , name):
    picture_path = os.path.join(app.root_path , 'static', 'productsDB' , name )
    image.save(picture_path)
    return image

def delete_image(name):
    picture_path = os.path.join(app.root_path, 'static', 'productsDB', name)
    os.remove(picture_path)
