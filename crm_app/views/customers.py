"""
Views für Kunden-bezogene Routen
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from models import db, Customer, Order, Contact
from datetime import datetime, date
from sqlalchemy import or_, func

customers_bp = Blueprint('customers', __name__, url_prefix='/customers')

ITEMS_PER_PAGE = 25


@customers_bp.route('/')
def list_customers():
    """Liste aller Kunden mit Suchfunktion und Pagination"""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '', type=str)
    sort_by = request.args.get('sort', 'name', type=str)  # name, last_contact
    
    # Basis-Query
    query = Customer.query
    
    # Suchfilter
    if search_query:
        search_pattern = f"%{search_query}%"
        query = query.filter(
            or_(
                Customer.first_name.ilike(search_pattern),
                Customer.last_name.ilike(search_pattern),
                Customer.email.ilike(search_pattern),
                Customer.phone.ilike(search_pattern)
            )
        )
    
    # Sortierung
    if sort_by == 'name':
        query = query.order_by(Customer.last_name, Customer.first_name)
    elif sort_by == 'last_contact':
        # Subquery für letzten Kontakt
        subquery = db.session.query(
            Contact.customer_id,
            func.max(Contact.contact_time).label('last_contact')
        ).group_by(Contact.customer_id).subquery()
        
        query = query.outerjoin(subquery, Customer.id == subquery.c.customer_id)\
                    .order_by(subquery.c.last_contact.desc().nullslast())
    
    # Pagination
    pagination = query.paginate(page=page, per_page=ITEMS_PER_PAGE, error_out=False)
    customers = pagination.items
    
    return render_template('customers/list.html',
                         customers=customers,
                         pagination=pagination,
                         search_query=search_query,
                         sort_by=sort_by)


@customers_bp.route('/<int:customer_id>')
def customer_detail(customer_id):
    """Detailansicht eines Kunden mit KPIs und Tabs"""
    customer = Customer.query.get_or_404(customer_id)
    
    # KPIs berechnen
    # 1. Gesamtumsatz
    total_revenue = customer.get_total_revenue()
    
    # 2. Umsatz letztes Jahr (2024)
    last_year_start = date(2024, 1, 1)
    last_year_end = date(2024, 12, 31)
    last_year_revenue = customer.get_total_revenue(last_year_start, last_year_end)
    
    # 3. Umsatz im gewählten Zeitraum (falls vorhanden)
    date_from = request.args.get('from', type=str)
    date_to = request.args.get('to', type=str)
    
    filtered_revenue = None
    if date_from and date_to:
        try:
            start_date = datetime.strptime(date_from, '%Y-%m-%d').date()
            end_date = datetime.strptime(date_to, '%Y-%m-%d').date()
            filtered_revenue = customer.get_total_revenue(start_date, end_date)
        except ValueError:
            pass  # Ungültiges Datumsformat
    
    # Letzte Bestellungen
    recent_orders = Order.query.filter_by(customer_id=customer_id)\
                               .order_by(Order.order_date.desc())\
                               .limit(10)\
                               .all()
    
    # Letzte Kontakte
    recent_contacts = Contact.query.filter_by(customer_id=customer_id)\
                                   .order_by(Contact.contact_time.desc())\
                                   .limit(10)\
                                   .all()
    
    # Anzahl Bestellungen und Kontakte
    order_count = Order.query.filter_by(customer_id=customer_id).count()
    contact_count = Contact.query.filter_by(customer_id=customer_id).count()
    
    return render_template('customers/detail.html',
                         customer=customer,
                         total_revenue=total_revenue,
                         last_year_revenue=last_year_revenue,
                         filtered_revenue=filtered_revenue,
                         date_from=date_from,
                         date_to=date_to,
                         recent_orders=recent_orders,
                         recent_contacts=recent_contacts,
                         order_count=order_count,
                         contact_count=contact_count)


@customers_bp.route('/<int:customer_id>/revenue')
def customer_revenue(customer_id):
    """API-Endpoint für Umsatzberechnung mit Datumsfilter"""
    customer = Customer.query.get_or_404(customer_id)
    
    date_from = request.args.get('from', type=str)
    date_to = request.args.get('to', type=str)
    
    if not date_from or not date_to:
        return jsonify({'error': 'Bitte Start- und Enddatum angeben'}), 400
    
    try:
        start_date = datetime.strptime(date_from, '%Y-%m-%d').date()
        end_date = datetime.strptime(date_to, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Ungültiges Datumsformat (erwartet: YYYY-MM-DD)'}), 400
    
    revenue = customer.get_total_revenue(start_date, end_date)
    
    return jsonify({
        'customer_id': customer_id,
        'customer_name': customer.full_name,
        'date_from': date_from,
        'date_to': date_to,
        'revenue': float(revenue)
    })


@customers_bp.route('/<int:customer_id>/orders')
def customer_orders(customer_id):
    """Alle Bestellungen eines Kunden"""
    customer = Customer.query.get_or_404(customer_id)
    page = request.args.get('page', 1, type=int)
    
    pagination = Order.query.filter_by(customer_id=customer_id)\
                           .order_by(Order.order_date.desc())\
                           .paginate(page=page, per_page=ITEMS_PER_PAGE, error_out=False)
    
    orders = pagination.items
    
    return render_template('customers/orders.html',
                         customer=customer,
                         orders=orders,
                         pagination=pagination)


@customers_bp.route('/<int:customer_id>/contacts')
def customer_contacts(customer_id):
    """Alle Kontakte eines Kunden"""
    customer = Customer.query.get_or_404(customer_id)
    page = request.args.get('page', 1, type=int)
    
    pagination = Contact.query.filter_by(customer_id=customer_id)\
                             .order_by(Contact.contact_time.desc())\
                             .paginate(page=page, per_page=ITEMS_PER_PAGE, error_out=False)
    
    contacts = pagination.items
    
    return render_template('customers/contacts.html',
                         customer=customer,
                         contacts=contacts,
                         pagination=pagination)


@customers_bp.route('/new', methods=['GET', 'POST'])
def new_customer():
    """Neuen Kunden erstellen"""
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        
        # Validierung
        if not first_name or not last_name:
            flash('Vorname und Nachname sind Pflichtfelder!', 'danger')
            return render_template('customers/new.html',
                                 first_name=first_name,
                                 last_name=last_name,
                                 email=email,
                                 phone=phone)
        
        # Prüfe ob E-Mail bereits existiert
        if email and Customer.query.filter_by(email=email).first():
            flash('Ein Kunde mit dieser E-Mail-Adresse existiert bereits!', 'warning')
            return render_template('customers/new.html',
                                 first_name=first_name,
                                 last_name=last_name,
                                 email=email,
                                 phone=phone)
        
        # Erstelle neuen Kunden
        new_customer = Customer(
            first_name=first_name,
            last_name=last_name,
            email=email if email else None,
            phone=phone if phone else None
        )
        
        try:
            db.session.add(new_customer)
            db.session.commit()
            flash(f'Kunde "{new_customer.full_name}" erfolgreich erstellt!', 'success')
            return redirect(url_for('customers.customer_detail', customer_id=new_customer.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Fehler beim Erstellen des Kunden: {str(e)}', 'danger')
            return render_template('customers/new.html',
                                 first_name=first_name,
                                 last_name=last_name,
                                 email=email,
                                 phone=phone)
    
    return render_template('customers/new.html')


@customers_bp.route('/<int:customer_id>/edit', methods=['GET', 'POST'])
def edit_customer(customer_id):
    """Kundendaten bearbeiten"""
    customer = Customer.query.get_or_404(customer_id)
    
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        
        # Validierung
        if not first_name or not last_name:
            flash('Vorname und Nachname sind Pflichtfelder!', 'danger')
            return render_template('customers/edit.html', customer=customer)
        
        # Prüfe ob E-Mail bereits von anderem Kunden verwendet wird
        if email:
            existing = Customer.query.filter_by(email=email).first()
            if existing and existing.id != customer_id:
                flash('Ein anderer Kunde verwendet bereits diese E-Mail-Adresse!', 'warning')
                return render_template('customers/edit.html', customer=customer)
        
        # Aktualisiere Kundendaten
        customer.first_name = first_name
        customer.last_name = last_name
        customer.email = email if email else None
        customer.phone = phone if phone else None
        
        try:
            db.session.commit()
            flash(f'Kunde "{customer.full_name}" erfolgreich aktualisiert!', 'success')
            return redirect(url_for('customers.customer_detail', customer_id=customer.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Fehler beim Aktualisieren des Kunden: {str(e)}', 'danger')
    
    return render_template('customers/edit.html', customer=customer)
