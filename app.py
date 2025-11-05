"""
Flask Haupt-Anwendung für das CRM System
Projekt: Einfaches CRM System - 5BHWI
"""

import os
from flask import Flask, render_template
from dotenv import load_dotenv
from models import db
import pytz

# Lade Umgebungsvariablen
load_dotenv()

def create_app():
    """Factory-Funktion zum Erstellen der Flask-App"""
    app = Flask(__name__,   
                template_folder='crm_app/templates',
                static_folder='crm_app/static')
    
    # Konfiguration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///crm.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TIMEZONE'] = pytz.timezone(os.getenv('TIMEZONE', 'Europe/Vienna'))
    
    # Jinja2-Filter für Zahlenformatierung (Deutsch/Österreich)
    @app.template_filter('currency')
    def currency_filter(value):
        """Formatiert einen Wert als Währung (EUR)"""
        if value is None:
            return '€ 0,00'
        return f"€ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    @app.template_filter('datetime_format')
    def datetime_format_filter(value, format='%d.%m.%Y %H:%M'):
        """Formatiert ein Datetime-Objekt nach deutschem Standard"""
        if value is None:
            return ''
        if hasattr(value, 'strftime'):
            return value.strftime(format)
        return value
    
    @app.template_filter('date_format')
    def date_format_filter(value):
        """Formatiert ein Datum nach deutschem Standard"""
        return datetime_format_filter(value, '%d.%m.%Y')
    
    @app.template_filter('relative_time')
    def relative_time_filter(value):
        """Formatiert ein Datetime als relative Zeit (z.B. '2d', '3h', '15min')"""
        if value is None:
            return '-'
        
        from datetime import datetime, timezone
        
        # Stelle sicher, dass wir ein timezone-aware datetime haben
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        
        now = datetime.now(timezone.utc)
        diff = now - value
        
        # Berechne die Differenz
        seconds = int(diff.total_seconds())
        
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes}min"
        elif seconds < 86400:
            hours = seconds // 3600
            return f"{hours}h"
        elif seconds < 604800:
            days = seconds // 86400
            return f"{days}d"
        elif seconds < 2592000:
            weeks = seconds // 604800
            return f"{weeks}w"
        elif seconds < 31536000:
            months = seconds // 2592000
            return f"{months}mo"
        else:
            years = seconds // 31536000
            return f"{years}y"
    
    # Initialisiere Datenbank
    db.init_app(app)
    
    # Registriere Blueprints
    from crm_app.views.customers import customers_bp
    from crm_app.views.orders import orders_bp
    from crm_app.views.contacts import contacts_bp
    
    app.register_blueprint(customers_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(contacts_bp)
    
    # Hauptroute - Dashboard
    @app.route('/')
    def index():
        """Dashboard mit Übersicht aller Kunden, Bestellungen und Kontakte"""
        from models import Customer, Order, Contact
        
        # Lade die letzten Einträge für das Dashboard
        recent_customers = Customer.query.order_by(Customer.created_at.desc()).limit(10).all()
        recent_orders = Order.query.order_by(Order.order_date.desc()).limit(10).all()
        recent_contacts = Contact.query.order_by(Contact.contact_time.desc()).limit(10).all()
        
        # Statistiken
        total_customers = Customer.query.count()
        total_orders = Order.query.count()
        total_contacts = Contact.query.count()
        
        # Gesamtumsatz
        total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
        
        return render_template('index.html',
                             recent_customers=recent_customers,
                             recent_orders=recent_orders,
                             recent_contacts=recent_contacts,
                             total_customers=total_customers,
                             total_orders=total_orders,
                             total_contacts=total_contacts,
                             total_revenue=total_revenue)
    
    @app.errorhandler(404)
    def page_not_found(e):
        """404-Fehlerseite"""
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        """500-Fehlerseite"""
        return render_template('500.html'), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    # Erstelle Datenbanktabellen, falls sie nicht existieren
    with app.app_context():
        db.create_all()
        print("Datenbank initialisiert!")
    
    # Starte den Entwicklungsserver
    app.run(debug=True, host='0.0.0.0', port=5000)
