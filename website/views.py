import shutil
import tempfile
from flask import Blueprint, render_template, send_file, url_for, json, flash, redirect, request, send_file, current_app, session
from .models import Tovar, Order, Point
from . import db
from sqlalchemy import func
from datetime import datetime
import os
from flask_admin import expose, AdminIndexView
from sqlalchemy import desc
from functools import wraps

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

@views.route('/karta')
def karta():
    total_quantity = get_items_cart()
    return render_template('karta.html', total_quantity=total_quantity)

class MyMainView(AdminIndexView):
    @expose('/')
    def admin_stats(self):
        base_path = os.path.abspath(os.path.join(os.path.dirname(__name__), 'website'))
        image_folder = os.path.join(base_path, 'static', 'img')
        video_folder = os.path.join(base_path, 'static', 'video')

        images = [url_for('static', filename=f'img/{image}') for image in os.listdir(image_folder)]
        videos = [url_for('static', filename=f'video/{image}') for image in os.listdir(video_folder)]
        
        num_images = len(images)
        num_videos = len(videos)

        tovar_data = Tovar.query.count()
        order_data = db.session.query(func.count(Order.nomerzakaza.distinct())).scalar()
        point_data = Point.query.count()

        return self.render('admin/stats.html', 
                           tovar_data=tovar_data,
                           order_data=order_data,
                           point_data=point_data,
                           images=images, 
                           videos=videos,
                           num_images=num_images,
                           num_videos=num_videos
                           )