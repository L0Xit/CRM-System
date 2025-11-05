"""
Views für Kontakt-bezogene Routen
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Contact, Customer, User
from datetime import datetime

contacts_bp = Blueprint('contacts', __name__, url_prefix='/contacts')

ITEMS_PER_PAGE = 50

# Verfügbare Kontaktarten
CONTACT_CHANNELS = ['Telefon', 'E-Mail', 'Meeting', 'Chat']


@contacts_bp.route('/')
def list_contacts():
    """Globale Kontaktübersicht mit Filterung und Pagination"""
    page = request.args.get('page', 1, type=int)
    channel_filter = request.args.get('channel', '', type=str)
    
    # Basis-Query mit JOIN auf Customer
    query = Contact.query.join(Customer)
    
    # Filter nach Kontaktart
    if channel_filter and channel_filter in CONTACT_CHANNELS:
        query = query.filter(Contact.channel == channel_filter)
    
    # Sortierung: Chronologisch, neueste zuerst
    query = query.order_by(Contact.contact_time.desc())
    
    # Pagination
    pagination = query.paginate(page=page, per_page=ITEMS_PER_PAGE, error_out=False)
    contacts = pagination.items
    
    return render_template('contacts/list.html',
                         contacts=contacts,
                         pagination=pagination,
                         channel_filter=channel_filter,
                         available_channels=CONTACT_CHANNELS)


@contacts_bp.route('/<int:contact_id>')
def contact_detail(contact_id):
    """Detailansicht eines Kontakts"""
    contact = Contact.query.get_or_404(contact_id)
    
    return render_template('contacts/detail.html',
                         contact=contact)


@contacts_bp.route('/new', methods=['GET', 'POST'])
def new_contact():
    """Neuen Kontakt erstellen"""
    if request.method == 'POST':
        customer_id = request.form.get('customer_id', type=int)
        user_id = request.form.get('user_id', type=int)
        channel = request.form.get('channel', '')
        subject = request.form.get('subject', '').strip()
        notes = request.form.get('notes', '').strip()
        contact_date = request.form.get('contact_date', '')
        contact_time = request.form.get('contact_time', '')
        
        # Validierung
        if not customer_id:
            flash('Bitte wählen Sie einen Kunden aus!', 'danger')
            customers = Customer.query.order_by(Customer.last_name, Customer.first_name).all()
            users = User.query.order_by(User.name).all()
            return render_template('contacts/new.html',
                                 customers=customers,
                                 users=users,
                                 channels=CONTACT_CHANNELS)
        
        if not channel or channel not in CONTACT_CHANNELS:
            flash('Bitte wählen Sie eine gültige Kontaktart aus!', 'danger')
            customers = Customer.query.order_by(Customer.last_name, Customer.first_name).all()
            users = User.query.order_by(User.name).all()
            return render_template('contacts/new.html',
                                 customers=customers,
                                 users=users,
                                 channels=CONTACT_CHANNELS,
                                 selected_customer_id=customer_id)
        
        # Erstelle Kontakt-Zeitpunkt
        if contact_date and contact_time:
            try:
                contact_datetime = datetime.strptime(f"{contact_date} {contact_time}", "%Y-%m-%d %H:%M")
            except ValueError:
                contact_datetime = datetime.utcnow()
        else:
            contact_datetime = datetime.utcnow()
        
        # Erstelle neuen Kontakt
        new_contact = Contact(
            customer_id=customer_id,
            user_id=user_id if user_id else None,
            channel=channel,
            subject=subject if subject else None,
            notes=notes if notes else None,
            contact_time=contact_datetime
        )
        
        try:
            db.session.add(new_contact)
            db.session.commit()
            
            customer = Customer.query.get(customer_id)
            flash(f'Kontakt mit {customer.full_name} erfolgreich erstellt!', 'success')
            return redirect(url_for('contacts.contact_detail', contact_id=new_contact.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Fehler beim Erstellen des Kontakts: {str(e)}', 'danger')
    
    # GET: Zeige Formular
    customers = Customer.query.order_by(Customer.last_name, Customer.first_name).all()
    users = User.query.order_by(User.name).all()
    
    # Wenn customer_id in URL, vorselektieren
    preselected_customer_id = request.args.get('customer_id', type=int)
    
    return render_template('contacts/new.html',
                         customers=customers,
                         users=users,
                         channels=CONTACT_CHANNELS,
                         selected_customer_id=preselected_customer_id)
