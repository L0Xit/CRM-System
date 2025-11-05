"""
SQLAlchemy Datenbankmodelle für das CRM System
Projekt: Einfaches CRM System - 5BHWI
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

db = SQLAlchemy()

# Timezone-Konfiguration für Österreich
VIENNA_TZ = pytz.timezone('Europe/Vienna')


def get_local_time():
    """Gibt die aktuelle Zeit in der Wiener Zeitzone zurück"""
    return datetime.now(VIENNA_TZ)


class Customer(db.Model):
    """Kundenmodell"""
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True)
    phone = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Beziehungen
    orders = db.relationship('Order', back_populates='customer', cascade='all, delete-orphan')
    contacts = db.relationship('Contact', back_populates='customer', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Customer {self.last_name}, {self.first_name}>'
    
    @property
    def full_name(self):
        """Vollständiger Name (Nachname, Vorname)"""
        return f"{self.last_name}, {self.first_name}"
    
    @property
    def last_contact_date(self):
        """Datum des letzten Kontakts"""
        if self.contacts:
            return max(contact.contact_time for contact in self.contacts)
        return None
    
    def get_total_revenue(self, start_date=None, end_date=None):
        """Berechnet den Gesamtumsatz für diesen Kunden im angegebenen Zeitraum"""
        query = db.session.query(db.func.sum(Order.total_amount)).filter(Order.customer_id == self.id)
        
        if start_date:
            query = query.filter(Order.order_date >= start_date)
        if end_date:
            query = query.filter(Order.order_date <= end_date)
        
        result = query.scalar()
        return float(result) if result else 0.0
    
    def get_customer_score(self):
        """
        Berechnet einen Kunden-Score (0-100) basierend auf:
        - Gesamtumsatz (40%)
        - Anzahl Bestellungen (30%)
        - Kontaktfrequenz (30%)
        
        Rückgabe: dict mit score, rating ('A+', 'A', 'B', 'C', 'D'), und color
        """
        from datetime import timedelta
        
        # 1. Umsatz-Score (0-40 Punkte)
        total_revenue = self.get_total_revenue()
        if total_revenue >= 10000:
            revenue_score = 40
        elif total_revenue >= 5000:
            revenue_score = 35
        elif total_revenue >= 2000:
            revenue_score = 30
        elif total_revenue >= 1000:
            revenue_score = 25
        elif total_revenue >= 500:
            revenue_score = 20
        elif total_revenue > 0:
            revenue_score = 15
        else:
            revenue_score = 0
        
        # 2. Bestellungs-Score (0-30 Punkte)
        order_count = len(self.orders)
        if order_count >= 20:
            order_score = 30
        elif order_count >= 10:
            order_score = 25
        elif order_count >= 5:
            order_score = 20
        elif order_count >= 3:
            order_score = 15
        elif order_count >= 1:
            order_score = 10
        else:
            order_score = 0
        
        # 3. Kontakt-Score (0-30 Punkte)
        if self.last_contact_date:
            days_since_contact = (datetime.utcnow() - self.last_contact_date).days
            if days_since_contact <= 7:
                contact_score = 30
            elif days_since_contact <= 30:
                contact_score = 25
            elif days_since_contact <= 90:
                contact_score = 20
            elif days_since_contact <= 180:
                contact_score = 15
            elif days_since_contact <= 365:
                contact_score = 10
            else:
                contact_score = 5
        else:
            contact_score = 0
        
        # Gesamtscore
        total_score = revenue_score + order_score + contact_score
        
        # Rating und Farbe
        if total_score >= 85:
            rating = 'A+'
            color = 'success'
            label = 'Premium'
        elif total_score >= 70:
            rating = 'A'
            color = 'success'
            label = 'Sehr gut'
        elif total_score >= 55:
            rating = 'B'
            color = 'info'
            label = 'Gut'
        elif total_score >= 40:
            rating = 'C'
            color = 'warning'
            label = 'Normal'
        else:
            rating = 'D'
            color = 'danger'
            label = 'Inaktiv'
        
        return {
            'score': total_score,
            'rating': rating,
            'color': color,
            'label': label,
            'revenue_score': revenue_score,
            'order_score': order_score,
            'contact_score': contact_score
        }


class Order(db.Model):
    """Bestellungsmodell"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Offen')
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Beziehungen
    customer = db.relationship('Customer', back_populates='orders')
    items = db.relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    
    # Indizes
    __table_args__ = (
        db.Index('idx_order_date', 'order_date'),
        db.Index('idx_customer_order_date', 'customer_id', 'order_date'),
    )
    
    def __repr__(self):
        return f'<Order {self.id} - {self.customer.full_name if self.customer else "N/A"}>'
    
    @property
    def item_count(self):
        """Anzahl der Positionen in der Bestellung"""
        return len(self.items)


class OrderItem(db.Model):
    """Bestellpositionsmodell"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Beziehungen
    order = db.relationship('Order', back_populates='items')
    product = db.relationship('Product', back_populates='order_items')
    
    def __repr__(self):
        return f'<OrderItem {self.id} - {self.quantity}x {self.product.name if self.product else "N/A"}>'
    
    @property
    def subtotal(self):
        """Zwischensumme (Menge * Einzelpreis)"""
        return float(self.quantity * self.unit_price)


class Product(db.Model):
    """Produktmodell"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sku = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(255), nullable=False)
    base_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Beziehungen
    order_items = db.relationship('OrderItem', back_populates='product')
    
    def __repr__(self):
        return f'<Product {self.sku} - {self.name}>'


class Contact(db.Model):
    """Kontaktmodell"""
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    channel = db.Column(db.String(20), nullable=False)  # Telefon, E-Mail, Meeting, Chat
    subject = db.Column(db.String(255))
    notes = db.Column(db.Text)
    contact_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Beziehungen
    customer = db.relationship('Customer', back_populates='contacts')
    user = db.relationship('User', back_populates='contacts')
    
    # Indizes
    __table_args__ = (
        db.Index('idx_contact_time', 'contact_time'),
        db.Index('idx_customer_contact_time', 'customer_id', 'contact_time'),
    )
    
    def __repr__(self):
        return f'<Contact {self.id} - {self.channel} - {self.customer.full_name if self.customer else "N/A"}>'


class User(db.Model):
    """Benutzermodell (Mitarbeiter/Schüler)"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.String(20), default='Schüler')  # Schüler, Lehrer
    
    # Beziehungen
    contacts = db.relationship('Contact', back_populates='user')
    
    def __repr__(self):
        return f'<User {self.name} - {self.role}>'
