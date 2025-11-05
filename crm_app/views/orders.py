"""
Views für Bestellungs-bezogene Routen
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Order, Customer, Product, OrderItem
from datetime import datetime
from decimal import Decimal
from sqlalchemy import or_, func

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

ITEMS_PER_PAGE = 50


@orders_bp.route('/')
def list_orders():
    """Globale Bestellungsübersicht mit Suchfunktion und Pagination"""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '', type=str)
    
    # Basis-Query mit JOIN auf Customer
    query = Order.query.join(Customer)
    
    # Suchfilter
    if search_query:
        search_pattern = f"%{search_query}%"
        # Suche nach Bestellnummer oder Kundenname
        query = query.filter(
            or_(
                func.cast(Order.id, db.String).ilike(search_pattern),
                Customer.first_name.ilike(search_pattern),
                Customer.last_name.ilike(search_pattern)
            )
        )
    
    # Sortierung: Chronologisch, neueste zuerst
    query = query.order_by(Order.order_date.desc())
    
    # Pagination
    pagination = query.paginate(page=page, per_page=ITEMS_PER_PAGE, error_out=False)
    orders = pagination.items
    
    return render_template('orders/list.html',
                         orders=orders,
                         pagination=pagination,
                         search_query=search_query)


@orders_bp.route('/<int:order_id>')
def order_detail(order_id):
    """Detailansicht einer Bestellung"""
    order = Order.query.get_or_404(order_id)
    
    return render_template('orders/detail.html',
                         order=order)


@orders_bp.route('/new', methods=['GET', 'POST'])
def new_order():
    """Neue Bestellung erstellen"""
    if request.method == 'POST':
        customer_id = request.form.get('customer_id', type=int)
        status = request.form.get('status', 'Offen')
        
        if not customer_id:
            flash('Bitte wählen Sie einen Kunden aus!', 'danger')
            customers = Customer.query.order_by(Customer.last_name, Customer.first_name).all()
            products = Product.query.order_by(Product.name).all()
            return render_template('orders/new.html', customers=customers, products=products)
        
        customer = Customer.query.get_or_404(customer_id)
        
        # Erstelle neue Bestellung
        new_order = Order(
            customer_id=customer_id,
            order_date=datetime.utcnow(),
            status=status,
            total_amount=Decimal('0.00')
        )
        
        # Verarbeite Bestellpositionen
        product_ids = request.form.getlist('product_id[]')
        quantities = request.form.getlist('quantity[]')
        
        total = Decimal('0.00')
        items_added = False
        
        for prod_id, qty in zip(product_ids, quantities):
            if prod_id and qty:
                try:
                    product = Product.query.get(int(prod_id))
                    quantity = int(qty)
                    
                    if product and quantity > 0:
                        item = OrderItem(
                            product_id=product.id,
                            quantity=quantity,
                            unit_price=product.base_price
                        )
                        new_order.items.append(item)
                        total += product.base_price * quantity
                        items_added = True
                except (ValueError, TypeError):
                    continue
        
        if not items_added:
            flash('Bitte fügen Sie mindestens eine Bestellposition hinzu!', 'warning')
            customers = Customer.query.order_by(Customer.last_name, Customer.first_name).all()
            products = Product.query.order_by(Product.name).all()
            return render_template('orders/new.html', 
                                 customers=customers, 
                                 products=products,
                                 selected_customer_id=customer_id)
        
        new_order.total_amount = total
        
        try:
            db.session.add(new_order)
            db.session.commit()
            flash(f'Bestellung #{new_order.id} für {customer.full_name} erfolgreich erstellt!', 'success')
            return redirect(url_for('orders.order_detail', order_id=new_order.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Fehler beim Erstellen der Bestellung: {str(e)}', 'danger')
    
    # GET: Zeige Formular
    customers = Customer.query.order_by(Customer.last_name, Customer.first_name).all()
    products = Product.query.order_by(Product.name).all()
    
    # Wenn customer_id in URL, vorselektieren
    preselected_customer_id = request.args.get('customer_id', type=int)
    
    return render_template('orders/new.html', 
                         customers=customers, 
                         products=products,
                         selected_customer_id=preselected_customer_id)
