"""
Datenbank-Initialisierung mit Testdaten
Projekt: Einfaches CRM System - 5BHWI

Führen Sie dieses Skript aus, um die Datenbank zu erstellen und mit Beispieldaten zu befüllen.
"""

import sys
import os
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Füge das Hauptverzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, Customer, Order, OrderItem, Product, Contact, User

def init_database():
    """Erstellt die Datenbank und füllt sie mit Testdaten"""
    app = create_app()
    
    with app.app_context():
        # Lösche alle bestehenden Tabellen und erstelle sie neu
        print("Erstelle Datenbanktabellen...")
        db.drop_all()
        db.create_all()
        
        # Füge Testdaten hinzu
        print("Füge Testdaten hinzu...")
        
        # Benutzer (Mitarbeiter)
        users = create_users()
        db.session.add_all(users)
        db.session.commit()
        print(f"✓ {len(users)} Benutzer erstellt")
        
        # Produkte
        products = create_products()
        db.session.add_all(products)
        db.session.commit()
        print(f"✓ {len(products)} Produkte erstellt")
        
        # Kunden
        customers = create_customers()
        db.session.add_all(customers)
        db.session.commit()
        print(f"✓ {len(customers)} Kunden erstellt")
        
        # Bestellungen mit Positionen
        orders = create_orders(customers, products)
        db.session.add_all(orders)
        db.session.commit()
        print(f"✓ {len(orders)} Bestellungen erstellt")
        
        # Kontakte
        contacts = create_contacts(customers, users)
        db.session.add_all(contacts)
        db.session.commit()
        print(f"✓ {len(contacts)} Kontakte erstellt")
        
        print("\n✅ Datenbank erfolgreich initialisiert!")
        print(f"\nStatistiken:")
        print(f"  - Kunden: {Customer.query.count()}")
        print(f"  - Bestellungen: {Order.query.count()}")
        print(f"  - Bestellpositionen: {OrderItem.query.count()}")
        print(f"  - Produkte: {Product.query.count()}")
        print(f"  - Kontakte: {Contact.query.count()}")
        print(f"  - Benutzer: {User.query.count()}")


def create_users():
    """Erstellt Testbenutzer"""
    users = [
        User(name="S. König", email="s.koenig@htl.at", role="Lehrer"),
        User(name="L. Graf", email="l.graf@htl.at", role="Schüler"),
        User(name="M. Müller", email="m.mueller@htl.at", role="Schüler"),
        User(name="A. Schmidt", email="a.schmidt@htl.at", role="Schüler"),
    ]
    return users


def create_products():
    """Erstellt Testprodukte"""
    products = [
        Product(sku="PROD-001", name="Produkt Alpha", base_price=Decimal("29.99")),
        Product(sku="PROD-002", name="Produkt Beta", base_price=Decimal("59.99")),
        Product(sku="PROD-003", name="Produkt Gamma", base_price=Decimal("99.99")),
        Product(sku="PROD-004", name="Produkt Delta", base_price=Decimal("149.99")),
        Product(sku="PROD-005", name="Produkt Epsilon", base_price=Decimal("199.99")),
        Product(sku="SERV-001", name="Dienstleistung Standard", base_price=Decimal("79.00")),
        Product(sku="SERV-002", name="Dienstleistung Premium", base_price=Decimal("159.00")),
        Product(sku="SOFT-001", name="Software Lizenz Basic", base_price=Decimal("49.00")),
        Product(sku="SOFT-002", name="Software Lizenz Pro", base_price=Decimal("129.00")),
        Product(sku="CONS-001", name="Beratungsstunde", base_price=Decimal("89.00")),
    ]
    return products


def create_customers():
    """Erstellt Testkunden"""
    first_names = ["Anna", "Max", "Sophie", "Lukas", "Emma", "Felix", "Laura", "Jonas", 
                   "Marie", "Paul", "Lena", "David", "Julia", "Michael", "Sarah"]
    last_names = ["Berger", "Huber", "Wagner", "Müller", "Schmidt", "Schneider", "Fischer", 
                  "Weber", "Meyer", "Bauer", "Becker", "Hoffmann", "Schulz", "Koch", "Richter"]
    
    customers = []
    for i in range(30):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            email=f"{first_name.lower()}.{last_name.lower()}{i}@example.com",
            phone=f"+43 {random.randint(600, 699)} {random.randint(100000, 999999)}",
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 730))
        )
        customers.append(customer)
    
    return customers


def create_orders(customers, products):
    """Erstellt Testbestellungen mit Positionen"""
    orders = []
    statuses = ["Offen", "In Bearbeitung", "Abgeschlossen", "Storniert"]
    
    for customer in customers:
        # Jeder Kunde bekommt 1-5 Bestellungen
        num_orders = random.randint(1, 5)
        
        for _ in range(num_orders):
            order_date = datetime.utcnow() - timedelta(days=random.randint(1, 365))
            order = Order(
                customer_id=customer.id,
                order_date=order_date,
                status=random.choice(statuses),
                total_amount=Decimal("0.00")  # Wird später berechnet
            )
            
            # Füge 1-4 Positionen zur Bestellung hinzu
            num_items = random.randint(1, 4)
            total = Decimal("0.00")
            
            for _ in range(num_items):
                product = random.choice(products)
                quantity = random.randint(1, 5)
                unit_price = product.base_price * Decimal(random.uniform(0.9, 1.1))  # Leichte Preisvariation
                
                item = OrderItem(
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=unit_price
                )
                order.items.append(item)
                total += unit_price * quantity
            
            order.total_amount = total.quantize(Decimal("0.01"))
            orders.append(order)
    
    return orders


def create_contacts(customers, users):
    """Erstellt Testkontakte"""
    contacts = []
    channels = ["Telefon", "E-Mail", "Meeting", "Chat"]
    subjects = [
        "Produktanfrage",
        "Support-Anfrage",
        "Beratungsgespräch",
        "Reklamation",
        "Angebot angefordert",
        "Feedback zum Service",
        "Technische Frage",
        "Vertragsverlängerung",
        "Neukundenberatung",
        "Follow-up",
    ]
    
    for customer in customers:
        # Jeder Kunde bekommt 2-8 Kontakte
        num_contacts = random.randint(2, 8)
        
        for _ in range(num_contacts):
            contact_time = datetime.utcnow() - timedelta(days=random.randint(1, 365))
            contact = Contact(
                customer_id=customer.id,
                user_id=random.choice(users).id if random.random() > 0.2 else None,
                channel=random.choice(channels),
                subject=random.choice(subjects),
                notes=f"Kontakt am {contact_time.strftime('%d.%m.%Y')} durchgeführt. " + 
                      random.choice([
                          "Kunde war sehr zufrieden.",
                          "Weitere Nachverfolgung erforderlich.",
                          "Angebot wurde erstellt.",
                          "Kunde hat Interesse an weiteren Produkten.",
                          "Technisches Problem wurde gelöst.",
                          "Termin für nächste Woche vereinbart.",
                      ]),
                contact_time=contact_time
            )
            contacts.append(contact)
    
    return contacts


if __name__ == "__main__":
    print("=" * 60)
    print("CRM System - Datenbank-Initialisierung")
    print("=" * 60)
    print()
    
    try:
        init_database()
    except Exception as e:
        print(f"\n❌ Fehler bei der Initialisierung: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
