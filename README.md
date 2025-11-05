# CRM System - 5BHWII Schülerprojekt

Ein Customer Relationship Management (CRM) System entwickelt mit Python Flask und SQLite.

## 📋 Inhaltsverzeichnis

- [Projektübersicht](#projektübersicht)
- [Funktionen](#funktionen)
- [Technologie-Stack](#technologie-stack)
- [Installation](#installation)
- [Deployment auf PythonAnywhere](#deployment-auf-pythonanywhere)
- [Benutzerhandbuch](#benutzerhandbuch)
- [Datenbank-Schema](#datenbank-schema)
- [Troubleshooting](#troubleshooting)
- [Bewertungskriterien](#bewertungskriterien)

---

## 🎯 Projektübersicht

Dieses CRM-System ermöglicht die Verwaltung von:
- **Kunden** mit vollständigen Kontaktdaten
- **Bestellungen** mit mehreren Positionen
- **Kontakten** (Telefon, E-Mail, Meeting, Chat)
- **Produkten** im Katalog
- **Benutzer** (Mitarbeiter/Schüler)

### Projekt-Informationen
- **Schule**: HTL - 5BHWII
- **Projekt**: Einfaches CRM System
- **Framework**: Python Flask
- **Datenbank**: SQLite
- **Lokalisierung**: Deutsch (Österreich)
- **Zeitzone**: Europe/Vienna
- **Deployment**: PythonAnywhere

---

## ✨ Funktionen

### Hauptfunktionen

#### 1. **Dashboard**
- Übersicht über alle Kunden, Bestellungen und Kontakte
- Statistiken: Gesamtanzahl und Gesamtumsatz
- Schnellzugriff auf die neuesten Einträge
- Suchfunktionen für alle Bereiche

#### 2. **Kundenübersicht**
- Suchfunktion nach Name, E-Mail oder Telefonnummer
- Sortierung nach Name oder letztem Kontakt
- Pagination (25 Einträge pro Seite)
- Klickbare Tabellenzeilen für schnellen Zugriff

#### 3. **Kunden-Detailansicht**
- **KPIs (Key Performance Indicators)**:
  - Gesamtumsatz
  - Umsatz 2024
  - Umsatz in gewähltem Zeitraum
- **Datumsfilter**: Flexible Umsatzanalyse nach Zeitraum
- **Tabs**:
  - Letzte Bestellungen
  - Letzte Kontakte (Timeline-Ansicht)
  - Stammdaten
- Kontaktinformationen und Statistiken

#### 4. **Bestellungsübersicht**
- Chronologische Liste (neueste zuerst)
- Suchfunktion nach Bestellnummer oder Kunde
- Anzeige von Status, Summe und Positionen
- Pagination (50 Einträge pro Seite)

#### 5. **Kontaktübersicht**
- Chronologische Liste (neueste zuerst)
- Filterung nach Kontaktart (Telefon, E-Mail, Meeting, Chat)
- Anzeige von Datum, Kunde, Betreff und Mitarbeiter
- Pagination (50 Einträge pro Seite)

### Technische Features
- ✅ Responsive Webdesign (Mobile-friendly)
- ✅ Deutsche Lokalisierung (Datum, Währung)
- ✅ Timezone-aware Datetime-Handling
- ✅ RESTful API-Endpoints
- ✅ SQLAlchemy ORM
- ✅ Bootstrap 5 UI Framework
- ✅ Pagination für große Datensätze
- ✅ Suchfunktionalität
- ✅ Datenfilterung und Sortierung

---

## 🛠 Technologie-Stack

### Backend
- **Python 3.9+**
- **Flask 3.0.0** - Web Framework
- **SQLAlchemy 2.0.0** - ORM
- **Flask-SQLAlchemy 3.1.0** - Flask-Integration
- **pytz 2023.3** - Timezone-Support

### Frontend
- **Bootstrap 5.3** - CSS Framework
- **Bootstrap Icons** - Icon-Set
- **Vanilla JavaScript** - Interaktivität

### Datenbank
- **SQLite** - Eingebettete Datenbank

### Deployment
- **PythonAnywhere** - Hosting-Plattform
- **WSGI** - Web Server Gateway Interface

---

## 📥 Installation

### Voraussetzungen

- Python 3.9 oder höher
- pip (Python Package Manager)
- Git (optional)

### Schritt 1: Projekt herunterladen

```bash
# Mit Git
git clone <repository-url>
cd Projekt_CRM

# Oder ZIP-Datei entpacken und in den Ordner wechseln
```

### Schritt 2: Virtuelle Umgebung erstellen

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Schritt 3: Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### Schritt 4: Umgebungsvariablen konfigurieren

```bash
# Kopiere die Beispiel-Datei
copy .env.example .env

# Bearbeite .env und setze einen sicheren SECRET_KEY
```

### Schritt 5: Datenbank initialisieren

```bash
python migrations/init_db.py
```

Dieses Skript erstellt:
- 30 Testkunden
- 10 Produkte
- 60-150 Bestellungen
- 60-240 Kontakte
- 4 Benutzer

### Schritt 6: Anwendung starten

```bash
python app.py
```

Die Anwendung ist nun unter **http://localhost:5000** erreichbar.

---

## 🚀 Deployment auf PythonAnywhere

### Schritt 1: PythonAnywhere-Account erstellen

1. Gehe zu [https://www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Erstelle einen kostenlosen Account
3. Verifiziere deine E-Mail-Adresse

### Schritt 2: Projekt hochladen

**Option A: Git (empfohlen)**
```bash
# In der PythonAnywhere Bash Console
cd ~
git clone <your-repository-url> Projekt_CRM
cd Projekt_CRM
```

**Option B: Manueller Upload**
1. Verwende "Files" Tab in PythonAnywhere
2. Lade alle Projektdateien hoch

### Schritt 3: Virtuelle Umgebung erstellen

```bash
cd ~/Projekt_CRM
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Schritt 4: Datenbank initialisieren

```bash
python migrations/init_db.py
```

### Schritt 5: Web App konfigurieren

1. Gehe zum "Web" Tab
2. Klicke "Add a new web app"
3. Wähle "Manual configuration"
4. Wähle Python 3.10

**WSGI-Datei bearbeiten:**
```python
import sys
import os

# Pfad zum Projekt
project_home = '/home/yourusername/Projekt_CRM'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Virtual Environment
activate_this = '/home/yourusername/Projekt_CRM/venv/bin/activate_this.py'
exec(open(activate_this).read(), {'__file__': activate_this})

# Import Flask App
from app import create_app
application = create_app()
```

### Schritt 6: Statische Dateien konfigurieren

In den Web-Einstellungen:
- URL: `/static/`
- Directory: `/home/yourusername/Projekt_CRM/crm_app/static`

### Schritt 7: Umgebungsvariablen setzen

In der WSGI-Datei oder in einer .env-Datei:
```python
os.environ['SECRET_KEY'] = 'your-production-secret-key'
os.environ['FLASK_ENV'] = 'production'
```

### Schritt 8: Reload & Testen

1. Klicke "Reload" im Web-Tab
2. Öffne deine App-URL: `https://yourusername.pythonanywhere.com`
3. Teste alle Funktionen

### Smoke Tests

Führe diese Tests nach dem Deployment durch:

✅ **Dashboard**
- Dashboard lädt ohne Fehler
- Statistiken werden angezeigt
- Alle drei Übersichten enthalten Daten

✅ **Kunden**
- Kundenliste lädt
- Suchfunktion funktioniert
- Kunden-Details öffnen sich
- KPIs werden korrekt berechnet

✅ **Bestellungen**
- Bestellungsliste lädt
- Bestelldetails zeigen Positionen

✅ **Kontakte**
- Kontaktliste lädt
- Filter nach Kontaktart funktioniert

---

## 📖 Benutzerhandbuch

### Navigation

Die Hauptnavigation bietet Zugriff auf:
- **Dashboard**: Startseite mit Übersichten
- **Kunden**: Kundenverwaltung
- **Bestellungen**: Bestellungsübersicht
- **Kontakte**: Kontaktverwaltung

### Dashboard verwenden

1. **Statistiken**: Oben werden wichtige Kennzahlen angezeigt
2. **Schnellsuche**: Jede Übersicht hat ein Suchfeld
3. **Details öffnen**: Klicken Sie auf einen Eintrag für Details

### Kunden verwalten

#### Kunden suchen
1. Gehe zu "Kunden"
2. Gebe Suchbegriff ein (Name, E-Mail, Telefon)
3. Klicke "Suchen"

#### Kunden-Details anzeigen
1. Klicke auf einen Kunden in der Liste
2. Siehe KPIs (Umsätze)
3. Wechsle zwischen Tabs:
   - **Bestellungen**: Alle Bestellungen des Kunden
   - **Kontakte**: Kommunikationshistorie
   - **Stammdaten**: Kundendaten

#### Umsatzanalyse mit Datumsfilter
1. Öffne Kunden-Details
2. Wähle "Von" und "Bis" Datum
3. Klicke "Anwenden"
4. Der gefilterte Umsatz wird in der gelben Karte angezeigt

### Bestellungen anzeigen

1. Gehe zu "Bestellungen"
2. Nutze Suchfeld für Bestellnummer oder Kunde
3. Klicke auf Bestellung für Details mit allen Positionen

### Kontakte filtern

1. Gehe zu "Kontakte"
2. Wähle Kontaktart aus Dropdown:
   - Telefon
   - E-Mail
   - Meeting
   - Chat
3. Klicke "Filtern"

### Pagination verwenden

- Nutze "Zurück" und "Weiter" Buttons
- Klicke auf Seitenzahlen für direkten Zugriff
- Info am Ende zeigt aktuelle Seite und Gesamtzahl

---

## 🗄 Datenbank-Schema

### Tabellen-Übersicht

#### `customers` - Kunden
| Feld | Typ | Beschreibung |
|------|-----|--------------|
| id | INTEGER | Primärschlüssel |
| first_name | VARCHAR(100) | Vorname |
| last_name | VARCHAR(100) | Nachname |
| email | VARCHAR(255) | E-Mail (unique) |
| phone | VARCHAR(50) | Telefonnummer |
| created_at | DATETIME | Erstellungsdatum |

#### `orders` - Bestellungen
| Feld | Typ | Beschreibung |
|------|-----|--------------|
| id | INTEGER | Primärschlüssel |
| customer_id | INTEGER | Fremdschlüssel → customers |
| order_date | DATETIME | Bestelldatum |
| status | VARCHAR(20) | Status (Offen, Abgeschlossen, etc.) |
| total_amount | DECIMAL(10,2) | Gesamtsumme |

**Indizes**: `order_date`, `customer_id + order_date`

#### `order_items` - Bestellpositionen
| Feld | Typ | Beschreibung |
|------|-----|--------------|
| id | INTEGER | Primärschlüssel |
| order_id | INTEGER | Fremdschlüssel → orders |
| product_id | INTEGER | Fremdschlüssel → products |
| quantity | INTEGER | Menge |
| unit_price | DECIMAL(10,2) | Einzelpreis |

#### `products` - Produkte
| Feld | Typ | Beschreibung |
|------|-----|--------------|
| id | INTEGER | Primärschlüssel |
| sku | VARCHAR(100) | Artikelnummer (unique) |
| name | VARCHAR(255) | Produktname |
| base_price | DECIMAL(10,2) | Basispreis |

#### `contacts` - Kontakte
| Feld | Typ | Beschreibung |
|------|-----|--------------|
| id | INTEGER | Primärschlüssel |
| customer_id | INTEGER | Fremdschlüssel → customers |
| user_id | INTEGER | Fremdschlüssel → users |
| channel | VARCHAR(20) | Kontaktart |
| subject | VARCHAR(255) | Betreff |
| notes | TEXT | Notizen |
| contact_time | DATETIME | Kontaktzeitpunkt |

**Indizes**: `contact_time`, `customer_id + contact_time`

#### `users` - Benutzer
| Feld | Typ | Beschreibung |
|------|-----|--------------|
| id | INTEGER | Primärschlüssel |
| name | VARCHAR(100) | Name |
| email | VARCHAR(255) | E-Mail (unique) |
| password_hash | VARCHAR(255) | Passwort-Hash |
| role | VARCHAR(20) | Rolle (Schüler, Lehrer) |

### Beziehungen

```
customers 1──n orders
orders 1──n order_items
products 1──n order_items
customers 1──n contacts
users 1──n contacts
```

---

## 🔧 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'flask'"

**Lösung:**
```bash
# Stelle sicher, dass die virtuelle Umgebung aktiviert ist
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Installiere Abhängigkeiten
pip install -r requirements.txt
```

### Problem: "OperationalError: no such table: customers"

**Lösung:**
```bash
# Initialisiere die Datenbank neu
python migrations/init_db.py
```

### Problem: "Internal Server Error" nach Deployment

**Lösung:**
1. Überprüfe Error-Logs in PythonAnywhere
2. Stelle sicher, dass alle Pfade korrekt sind
3. Überprüfe WSGI-Konfiguration
4. Prüfe ob Virtual Environment korrekt aktiviert ist

### Problem: CSS/JavaScript lädt nicht

**Lösung:**
1. Überprüfe Static Files Konfiguration in PythonAnywhere
2. URL: `/static/`
3. Directory: `/home/username/Projekt_CRM/crm_app/static`

### Problem: Datumsformat falsch

**Lösung:**
- Zeitzone in `.env` prüfen: `TIMEZONE=Europe/Vienna`
- Server neu starten

### Problem: Keine Daten im Dashboard

**Lösung:**
```bash
# Überprüfe ob Datenbank Einträge hat
python migrations/init_db.py
```

---

## 📊 Bewertungskriterien

### Punkteverteilung (100 Punkte)

| Kriterium | Punkte | Beschreibung |
|-----------|--------|--------------|
| **Datenbankdesign & Migrationen** | 10 | Korrektes Schema, Beziehungen, Indizes |
| **Funktionalität (Muss-Kriterien)** | 10 | Alle geforderten Features implementiert |
| **Codequalität & Struktur** | 10 | Sauberer, wartbarer Code, MVC-Pattern |
| **UI/UX & Usability** | 10 | Responsive Design, intuitive Bedienung |
| **Dokumentation & Setup** | 50 | README, Setup-Guide, Troubleshooting |
| **Präsentation & Setup-Demo** | 10 | Live-Demo des Deployments |

### Muss-Kriterien

✅ Globale Kundenübersicht mit Suchfunktion  
✅ Globale Bestellungsübersicht (chronologisch)  
✅ Globale Kontaktübersicht (chronologisch, filterbar)  
✅ Detaillierte Kundensicht mit KPIs  
✅ Umsatzberechnungen mit Datumsfiltern  
✅ Responsive Webdesign  
✅ Deutsche Lokalisierung  
✅ Timezone-aware Datetime  
✅ Pagination  
✅ Deployment auf PythonAnywhere  

---

## 📝 Projekt-Struktur

```
Projekt_CRM/
├── app.py                      # Flask Hauptanwendung
├── models.py                   # Datenbankmodelle
├── wsgi.py                     # WSGI Entry Point
├── requirements.txt            # Python-Abhängigkeiten
├── .env.example               # Beispiel Umgebungsvariablen
├── .gitignore                 # Git Ignore-Datei
├── README.md                  # Diese Datei
│
├── crm_app/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── customers.py       # Kunden-Routes
│   │   ├── orders.py          # Bestellungs-Routes
│   │   └── contacts.py        # Kontakt-Routes
│   │
│   ├── templates/
│   │   ├── base.html          # Basis-Template
│   │   ├── index.html         # Dashboard
│   │   ├── customers/
│   │   │   ├── list.html      # Kundenliste
│   │   │   └── detail.html    # Kundendetails
│   │   ├── orders/
│   │   │   ├── list.html      # Bestellungsliste
│   │   │   └── detail.html    # Bestelldetails
│   │   └── contacts/
│   │       ├── list.html      # Kontaktliste
│   │       └── detail.html    # Kontaktdetails
│   │
│   └── static/
│       ├── css/
│       │   └── style.css      # Custom CSS
│       └── js/
│           └── main.js        # Custom JavaScript
│
└── migrations/
    └── init_db.py             # Datenbank-Initialisierung
```

---

## 👥 Autoren

**5BHWII Schülerprojekt**  
HTL - Software-Praktikum

---

## 📄 Lizenz

Dieses Projekt ist ein Schülerprojekt für Bildungszwecke.

---

## 🔗 Nützliche Links

- [Flask Dokumentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Dokumentation](https://docs.sqlalchemy.org/)
- [Bootstrap Dokumentation](https://getbootstrap.com/docs/)
- [PythonAnywhere Help](https://help.pythonanywhere.com/)

---

**Stand**: Oktober 2024  
**Version**: 1.0.0
