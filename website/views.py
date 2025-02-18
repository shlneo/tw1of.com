from flask import Blueprint, render_template, session
from .models import Tovar, Order, Point
from datetime import datetime
from sqlalchemy import desc

views = Blueprint('views', __name__)
current_date = datetime.now().date()

def get_items_cart():
    total_quantity = session.get('total_quantity', 0) 
    return total_quantity

@views.route('/')
def catalog():
    total_quantity = session.get('total_quantity', 0) 
    tovar_list = Tovar.query.order_by(desc(Tovar.status)).all()
    return render_template('catalog.html', 
                           total_quantity=total_quantity,
                        tovar_list=tovar_list)

@views.route('/product/<name>')
def product(name):
    total_quantity = get_items_cart()
    tovar = Tovar.query.filter_by(name=name).first()
    if tovar is None:
        return render_template('error.html'), 404
    return render_template('product.html', 
                        tovar=tovar,
                        total_quantity = total_quantity)
  
@views.route('/cart')
def cart():
    point = Point.query.all()
    session_cart = session.get('cart', [])

    cart = []
    for item in session_cart:
        tovar = Tovar.query.filter_by(name=item['tovar_name']).first()
        if tovar:
            cart.append({
                'tovar_name': item['tovar_name'],
                'quantity': item['quantity'],
                'price': item['price'],
                'img_name': tovar.img_name
            })

    items_count = len(cart)
    total_price = session.get('total_price', 0) 
    total_quantity = session.get('total_quantity', 0) 

    total_price_dbE = session.get('total_price_dbE', 0) 
    total_price_ddE = session.get('total_price_ddE', 0) 
    total_price_wws = session.get('total_price_wws', 0) 

    return render_template('cart.html', 
                           cart=cart,
                           items_count=items_count,
                           point=point,
                           total_price_dbE=total_price_dbE,
                           total_price_ddE=total_price_ddE,
                           total_price_wws=total_price_wws,
                           total_price=total_price, 
                           total_quantity=total_quantity)

@views.route('/faq')
def faq():
    total_quantity = get_items_cart()
    return render_template('FAQ.html', total_quantity=total_quantity)

@views.route('/info')
def info():
    total_quantity = get_items_cart()
    return render_template('info.html', total_quantity=total_quantity)

@views.route('/privacy')
def privacy():
    total_quantity = get_items_cart()
    return render_template('privacy.html', total_quantity=total_quantity)

@views.route('/offer')
def offer():
    total_quantity = get_items_cart()
    return render_template('offer.html', total_quantity=total_quantity)

