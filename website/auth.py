from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, login_user, logout_user
from .models import Tovar, Order, Point, User
import requests
from . import db
from user_agents import parse
from sqlalchemy import func
from flask import session
from werkzeug.security import check_password_hash
from .api_keys import *

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('admin.index')) 
        flash('error', 'error')

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.catalog'))

def get_location_info(user_agent_string):
    try:
        ip_response = requests.get("https://api64.ipify.org?format=json")
        ip_response.raise_for_status()
        ip_address = ip_response.json().get("ip")

        location_response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        location_response.raise_for_status()
        location_data = location_response.json()

        user_agent = parse(user_agent_string)
        browser = user_agent.browser.family 
        os = user_agent.os.family
        
        location = location_data.get("city", "None") + ", " + location_data.get("region", "None") + ", " + location_data.get("country", "None")
        ip_address_str = ip_address if ip_address else "None"

        return ip_address_str, location, os, browser

    except Exception as e:
        print(f"Error when receiving location data: {e}")
        return "None", "None", "None", "None"

def send_email(order_details, recipient_email, location=None, device=None, browser=None, ip_address=None):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    sender = EMAILNAME
    password = EMAILPASS

    order_table = """
        <table style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr style="background-color: #028dff; color: #fff;">
                    <th style="padding: 8px; border: 1px solid #ddd;">Item</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">Quantity</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">Price</th>
                </tr>
            </thead>
            <tbody>
        """
    for item in order_details['items']:
        order_table += f"""
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">{item['tovar_name']}</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{item['quantity']}</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{item['price']}</td>
            </tr>
        """
    order_table += """
        </tbody>
    </table>
    """
    
    order_details_section = f"""
    <div class="info">
        <p><strong>Order Number:</strong> {order_details['nomerzakaza']}</p>
        <p><strong>Delivery Type:</strong> {order_details['type']}</p>
        <p><strong>Customer Name:</strong> {order_details['fio']}</p>
        <p><strong>Email:</strong> {order_details['email']}</p>
        <p><strong>Telephone:</strong> {order_details['telephone']}</p>
        <p><strong>Receiving Point:</strong> {order_details['receiving_point'] or 'N/A'}</p>
        <p><strong>Address:</strong> {order_details['street']} {order_details['house']}
        {f"Apartment {order_details['flat']}" if order_details['flat'] else ''}</p>
        <p><strong>City:</strong> {order_details['city']}</p>
        <p><strong>Country:</strong> {order_details['country']}</p>
        <p><strong>Comment:</strong> {order_details['comment'] or 'No comment'}</p>
        <p><strong>Promo Code:</strong> {order_details['promocod'] or 'N/A'}</p>
    </div>
    """
    final_message = f"""
    <p>Here are the details of your order:</p>
    {order_details_section}
    <p>Items in your order:</p>
    {order_table}
    """
    base_styles = """
    <style>
        body { font-family: Arial, sans-serif; background-color: #f3f3f3; margin: 0; padding: 0; }
        .email-container { max-width: 600px; margin: 20px auto; background-color: #fff; border-radius: 8px;
                           overflow: hidden; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); }
        .header { background-color: #f3f3f3; text-align: center; padding: 20px; }
        .header a { font-size: 32px; font-weight: bold; padding: 15px; margin: 5px 0; }
        .content { padding: 20px; color: #333; }
        .info { background-color: #f9f9f9; padding: 15px; border-left: 4px solid #028dff; margin: 20px 0;
                border-radius: 4px; }
        .footer { background-color: #f3f3f3; padding: 10px; text-align: center; font-size: 12px; color: #777; }
        .footer a { color: #6441a5; text-decoration: none; }
    </style>
    """
    content = f"""
        <p>Hello {order_details['fio']},</p>
        <p>Thank you for your order.</p>
        <div class="info">
            {f'<p><strong>Location:</strong> {location}</p>' if location else ''}
            {f'<p><strong>Device:</strong> {device}</p>' if device else ''}
            {f'<p><strong>Browser:</strong> {browser}</p>' if browser else ''}
            {f'<p><strong>IP-address:</strong> {ip_address}</p>' if ip_address else ''}
        </div>
        {final_message}
        <p>If you have any questions, please contact our support team.</p>
    """
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>{base_styles}</head>
    <body>
        <div class="email-container">
            <div class="header"><a>shln</a></div>
            <div class="content">
                {content}
            </div>
            <div class="footer">
                <p>Additional information can be found <a href="https://shlnof.pythonanywhere.com">here</a>.</p>
                <p>Thanks,<br>Support Service shln</p>
            </div>
        </div>
    </body>
    </html>
    """
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try: 
        server.login(sender, password)
        
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = recipient_email
        msg["Subject"] = "Уведомление от Erespondent-Online"
        
        msg.attach(MIMEText(html_template, "html"))

        server.sendmail(sender, recipient_email, msg.as_string())

        return "Email sent successfully"
    except Exception as _ex:
        return f"{_ex}\nCheck log ..."
    finally:
        server.quit()

        

@auth.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    tovar_name = request.form.get('tovar_name')
    quantity = int(request.form.get('tovar_count'))
    price = float(request.form.get('tovar_cost'))

    tovar = Tovar.query.filter_by(name=tovar_name).first()
    if not tovar or tovar.count <= 0:
        flash(f'Out of stock {tovar_name}', category='error')
        return redirect(url_for('views.product', name=tovar_name))

    if 'cart' not in session:
        session['cart'] = []
        session['total_price'] = 0  
        session['total_quantity'] = 0  
        session['total_price_dbE'] = 0 
        session['total_price_ddE'] = 0 
        session['total_price_wws'] = 0 

    cart = session['cart']
    existing_item = next((item for item in cart if item['tovar_name'] == tovar_name), None)

    if existing_item:
        if existing_item['quantity'] + quantity <= tovar.count:
            existing_item['quantity'] += quantity
            existing_item['price'] = existing_item['quantity'] * existing_item['price_per_unit']
        else:
            flash(f'Not enough {tovar_name} in stock', category='error')
            return redirect(url_for('views.product', name=tovar_name))
    else:
        if quantity <= tovar.count:
            cart.append({
                'tovar_id': tovar.id,
                'tovar_name': tovar_name,
                'quantity': quantity,
                'price': round(price, 2),
                'price_per_unit': round(price / quantity, 2),
                'img_name': tovar.img_name
            })
        else:
            flash(f'Недостаточно {tovar_name} на складе', category='error')
            return redirect(url_for('views.product', name=tovar_name))

    total_price = sum(item['price'] for item in cart)
    total_quantity = sum(item['quantity'] for item in cart)

    session['cart'] = cart
    session['total_price'] = round(total_price, 2)  
    session['total_price_dbE'] = round(session['total_price'] + 2.50, 2)  
    session['total_price_ddE'] = round(session['total_price'] + 4.50, 2)  
    session['total_price_wws'] = round(session['total_price'] + 7.50, 2)  
    
    session['total_quantity'] = total_quantity 
    session.modified = True

    flash('The product has been added to the cart', category='success')
    return redirect(url_for('views.product', name=tovar_name))

@auth.route('/cart', methods=['GET', 'POST'])
def createorder():
    if request.method == 'POST':
        if 'cart' not in session or not session['cart']:
            flash('Your cart is empty. Add items to your cart before placing an order.', category='error')
            return redirect(url_for('views.cart'))
        
        items = session['cart']

        max_nomerzakaza = db.session.query(func.max(Order.nomerzakaza)).scalar()
        nomerzakaza = max_nomerzakaza + 1 if max_nomerzakaza is not None else 1

        email = request.form.get('email')
        fio = request.form.get('fio')
        telephone = request.form.get('telephone')
        receiving_point = request.form.get('receiving_point')
        country = request.form.get('country')
        city = request.form.get('cityInput')
        street = request.form.get('street')
        house = request.form.get('house')
        flat = request.form.get('flat')
        comment = request.form.get('comment')
        promocod = request.form.get('promocod')

        if receiving_point:
            type = 'Delivery across the RB to the branch (Evropochta)'
            current_point = Point.query.filter_by(number=receiving_point).first()
            current_point_id = current_point.id if current_point else None
        elif country != 'Belarus' or city:
            type = 'Worldwide shipping'
            current_point_id = None
        else:
            type = "Door-to-door delivery in the RB (Evropochta)"
            current_point_id = None

        order_details = {
            "nomerzakaza": nomerzakaza,
            "type": type,
            "fio": fio,
            "email": email,
            "telephone": telephone,
            "receiving_point": receiving_point,
            "street": street,
            "house": house,
            "flat": flat,
            "city": city,
            "country": country,
            "comment": comment,
            "promocod": promocod,
            "items": items 
        }

        for item in items:
            new_order = Order(
                nomerzakaza=nomerzakaza,
                type=type,
                fio=fio,
                email=email,
                telephone=telephone,
                receiving_point=current_point_id,
                street=street,
                house=house,
                flat=flat,
                city=city,
                country=country,
                comment=comment,
                promocod=promocod,
                price=item['price'],
                tovar_id=item['tovar_id'],
                tovar_quantity=item['quantity']
            )
            db.session.add(new_order)

            tovar = Tovar.query.filter_by(name=item['tovar_name']).first()
            if tovar:
                tovar.count -= item['quantity']
                if tovar.count <= 0:
                    tovar.count = 0
                    tovar.status = "Sold"
                db.session.commit()

        user_agent_string = request.headers.get('User-Agent')
        ip_address, location, os, browser = get_location_info(user_agent_string)

        send_email(order_details, email, location=location, device=os, browser=browser, ip_address=ip_address)

        session.pop('cart', None)
        session.pop('total_price', None)
        session.pop('total_price_dbE', None)
        session.pop('total_price_ddE', None)
        session.pop('total_price_wws', None)
        session.pop('total_quantity', None)
        flash('Order created successfully!', category='success')
    return redirect(url_for('views.cart'))


@auth.route('/update_cart', methods=['POST'])
def update_cart():
    try:
        data = request.get_json()
        product_name = data.get('tovar_name')
        new_quantity = data.get('quantity')

        if not product_name or new_quantity is None:
            return jsonify({'error': 'Invalid input'}), 400
        
        session_cart = session.get('cart', [])
        for item in session_cart:
            if item['tovar_name'] == product_name:
                item['quantity'] = new_quantity
                item['price'] = round(item['price_per_unit'] * new_quantity, 2)
                break

        total_price = sum(item['price'] for item in session_cart)
        total_quantity = sum(item['quantity'] for item in session_cart)

        session['cart'] = session_cart
        session['total_price'] = round(total_price, 2)
        session['total_price_dbE'] = round(total_price + 2.50, 2)  
        session['total_price_ddE'] = round(total_price + 4.50, 2)  
        session['total_price_wws'] = round(total_price + 7.50, 2)  
        session['total_quantity'] = total_quantity
        session.modified = True

        return jsonify({
            'success': True,
            'cart': session_cart,
            'total_price': session['total_price'],
            'total_quantity': session['total_quantity'],
            'total_price_dbE': session['total_price_dbE'],
            'total_price_ddE': session['total_price_ddE'],
            'total_price_wws': session['total_price_wws']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@auth.route('/remove_item', methods=['POST'])
def remove_item():
    try:
        data = request.get_json()
        product_name = data.get('tovar_name')

        if not product_name:
            return jsonify({'error': 'Invalid input'}), 400

        session_cart = session.get('cart', [])
        session_cart = [item for item in session_cart if item['tovar_name'] != product_name]

        total_price = sum(item['price'] for item in session_cart)
        total_quantity = sum(item['quantity'] for item in session_cart)

        session['cart'] = session_cart
        session['total_price'] = round(total_price, 2)
        session['total_price_dbE'] = round(total_price + 2.50, 2)  
        session['total_price_ddE'] = round(total_price + 4.50, 2)  
        session['total_price_wws'] = round(total_price + 7.50, 2) 

        session['total_quantity'] = total_quantity
        session.modified = True

        return jsonify({
            'success': True,
            'cart': session_cart,
            'total_price': session['total_price'],
            'total_quantity': session['total_quantity'],
            'total_price_dbE': session['total_price_dbE'],
            'total_price_ddE': session['total_price_ddE'],
            'total_price_wws': session['total_price_wws']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500