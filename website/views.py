import shutil
import tempfile
from flask import Blueprint, render_template, send_file, url_for, json, flash, redirect, request, send_file, current_app, session
from .models import Tovar, Order, Point
from . import db
import googlemaps
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
                           total_price=total_price,  # Передаем total_price в шаблон
                           total_quantity=total_quantity)  # Передаем total_quantity в шаблон


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

# @views.route('/map', methods=['GET', 'POST'])
# @login_required
# def map():
#     orders = Order.query.filter_by().first()
#     if not orders: 
#         flash('No active orders')
#         return render_template('catalog.html', user=current_user)
#     else:
#         with open("api.txt", "r") as api_file:
#             api_key = api_file.read().strip()
#         maps_client = googlemaps.Client(key=api_key)
#         order = None
#         if request.method == 'POST':
#             nomerzakaza = request.form.get('nomerzakaza')
#             order = Order.query.filter_by(nomerzakaza=nomerzakaza).first()
#         else:
#             order = Order.query.first()
#         A = "Налибокская 14, Минск"
#         A1 = "Nalibokskaya 14, Minsk"
#         if order:
#             if order.type == 'Delivery across the RB to the branch (Evropochta)':
#                 B = f"Налибокская 18"     
#             elif order.type == 'Door-to-door delivery in the RB (Evropochta)':
#                 B = f"{order.receiving_point}"     
#             elif order.type == 'Worldwide shipping':
#                 B = f"{order.street} {order.house}, {order.city}" 
#             geocode_resstrt1 = maps_client.geocode(A)
#             geocode_resstrt2 = maps_client.geocode(B)
#             if geocode_resstrt1 and geocode_resstrt2:
#                 lat1, lng1 = geocode_resstrt1[0]['geometry']['location']['lat'], geocode_resstrt1[0]['geometry']['location']['lng']
#                 lat2, lng2 = geocode_resstrt2[0]['geometry']['location']['lat'], geocode_resstrt2[0]['geometry']['location']['lng']
#                 origin = {'lat': lat1, 'lng': lng1}
#                 destination = {'lat': lat2, 'lng': lng2}
#                 driving_directions = maps_client.directions(A, B, mode="driving")
#                 walking_directions = maps_client.directions(A, B, mode="walking")
#                 bicycling_directions = maps_client.directions(A, B, mode="bicycling")
#                 transit_directions = maps_client.directions(A, B, mode="transit")
#                 driving_distance = driving_directions[0]['legs'][0]['distance']['text'] if driving_directions else "-"
#                 walking_distance = walking_directions[0]['legs'][0]['distance']['text'] if walking_directions else "-"
#                 bicycling_distance = bicycling_directions[0]['legs'][0]['distance']['text'] if bicycling_directions else "-"
#                 transit_distance = transit_directions[0]['legs'][0]['distance']['text'] if transit_directions else "-"
#                 HrsMinsDurationDriving = driving_directions[0]['legs'][0]['duration']['text'] if driving_directions else "-"
#                 HrsMinsDurationWalking = walking_directions[0]['legs'][0]['duration']['text'] if walking_directions else "-"
#                 HrsMinsDurationBicycling = bicycling_directions[0]['legs'][0]['duration']['text'] if bicycling_directions else "-"
#                 HrsMinsDurationTransit = transit_directions[0]['legs'][0]['duration']['text'] if transit_directions else "-"
#                 return render_template('karta.html',
#                                     order=order,
#                                     user=current_user,
#                                     api_key=api_key,
#                                     origin=origin,
#                                     destination=destination,
#                                     A1=A1,
#                                     A=A,
#                                     B=B,
#                                     driving_distance=driving_distance,
#                                     walking_distance=walking_distance,
#                                     bicycling_distance=bicycling_distance,
#                                     transit_distance=transit_distance,
#                                     HrsMinsDurationDriving=HrsMinsDurationDriving,
#                                     HrsMinsDurationWalking=HrsMinsDurationWalking,
#                                     HrsMinsDurationBicycling=HrsMinsDurationBicycling,
#                                     HrsMinsDurationTransit=HrsMinsDurationTransit)
#             else:
#                 flash('geocode_resstrt1 and geocode_resstrt2')
#                 return redirect(url_for('views.map'))
#         else:
#             flash('Some trubles')
#             return redirect(url_for('views.map'))


# def admin_only(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if current_user.type != 'Администратор':
#             flash('Недостаточно прав для входа в админ-панель', 'error')
#             return redirect(url_for('views.beginPage'))   
#         return f(*args, **kwargs)
#     return decorated_function


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
    
    # @admin_only
    @expose('/backup')
    def backup_database(self):
        try:
            database_path = current_app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')

            if not os.path.exists(database_path):
                flash('Файл базы данных не найден.', 'error')
                return redirect(request.referrer or url_for('admin.index'))

            with tempfile.NamedTemporaryFile(delete=False, suffix='.sqlite') as temp_file:
                shutil.copy2(database_path, temp_file.name)
                temp_file_path = temp_file.name

            flash('Резервная копия базы данных успешно создана.', 'success')
            return send_file(temp_file_path, as_attachment=True, download_name=f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sqlite")

        except Exception as e:
            flash(f'Ошибка при создании резервной копии базы данных: {str(e)}', 'error')
            return redirect(request.referrer or url_for('admin.index'))
