# 🚀 CRM System auf PythonAnywhere deployen

Diese Anleitung beschreibt Schritt für Schritt, wie Sie Ihr CRM-System auf PythonAnywhere hosten.

## 📋 Voraussetzungen

- Ein kostenloses PythonAnywhere-Konto: https://www.pythonanywhere.com/registration/register/beginner/
- Ihr CRM-Projekt lokal bereit
- Git installiert (optional, aber empfohlen)

---

## 🔧 Schritt 1: PythonAnywhere-Konto erstellen

1. Gehen Sie zu https://www.pythonanywhere.com/
2. Klicken Sie auf **"Start running Python online in less than a minute!"**
3. Wählen Sie den **Beginner Account** (kostenlos)
4. Registrieren Sie sich mit Ihrer E-Mail-Adresse
5. Bestätigen Sie Ihre E-Mail
6. Loggen Sie sich ein

---

## 📁 Schritt 2: Projekt-Dateien hochladen

### Option A: Mit Git (empfohlen)

1. **Erstellen Sie ein GitHub Repository:**
   - Gehen Sie zu https://github.com/new
   - Repository-Name: `crm-system`
   - Privat oder Öffentlich (Ihre Wahl)
   - Erstellen Sie das Repository

2. **Lokales Projekt zu Git hinzufügen:**
   ```bash
   cd C:\Users\user\Documents\Schule\5BHWII\SWP_Gruber\Projekt_CRM
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/IHR_USERNAME/crm-system.git
   git push -u origin main
   ```

3. **In PythonAnywhere clonen:**
   - Klicken Sie auf **"Consoles"** → **"Bash"**
   - Führen Sie aus:
   ```bash
   git clone https://github.com/IHR_USERNAME/crm-system.git
   cd crm-system
   ```

### Option B: Manuell hochladen

1. Klicken Sie auf **"Files"** in der PythonAnywhere-Navigation
2. Navigieren Sie zu Ihrem Home-Verzeichnis: `/home/IHR_USERNAME/`
3. Erstellen Sie einen neuen Ordner: `crm-system`
4. Laden Sie alle Projektdateien hoch:
   - `app.py`
   - `models.py`
   - `requirements.txt` (erstellen, siehe unten)
   - Ordner `crm_app/` (mit allen Unterordnern)
   - `.env` (Datei, siehe unten)

---

## 📦 Schritt 3: requirements.txt erstellen

Erstellen Sie eine Datei `requirements.txt` im Hauptverzeichnis mit folgendem Inhalt:

```txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
SQLAlchemy==2.0.23
python-dotenv==1.0.0
Werkzeug==3.0.1
pytz==2023.3
```

Diese Datei hochladen oder in der PythonAnywhere-Console erstellen:

```bash
cd ~/crm-system
nano requirements.txt
# Inhalt einfügen, Strg+X, Y, Enter zum Speichern
```

---

## 🔐 Schritt 4: Umgebungsvariablen einrichten

Erstellen Sie eine `.env` Datei:

```bash
cd ~/crm-system
nano .env
```

Fügen Sie folgenden Inhalt ein:

```env
SECRET_KEY=ihr-super-geheimer-produktions-key-hier-12345
SQLALCHEMY_DATABASE_URI=sqlite:///crm.db
TIMEZONE=Europe/Vienna
```

**Wichtig:** Ersetzen Sie `ihr-super-geheimer-produktions-key-hier-12345` mit einem echten zufälligen String!

Generieren Sie einen sicheren Key in der Python-Console:

```python
import secrets
print(secrets.token_hex(32))
```

Speichern Sie mit `Strg+X`, dann `Y`, dann `Enter`.

---

## 🐍 Schritt 5: Python-Pakete installieren

Sie haben zwei Optionen:

### 🎯 Option A: Einfach - Global installieren (empfohlen für Schulprojekte)

```bash
cd ~/crm-system
pip3.10 install --user --upgrade pip
pip3.10 install --user -r requirements.txt
```

**Vorteile:** Schnell, einfach, für ein einzelnes Projekt ausreichend

### 🔧 Option B: Mit Virtual Environment (Best Practice)

```bash
cd ~/crm-system
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Vorteile:** Saubere Trennung, professioneller, bei mehreren Projekten besser

---

**Überprüfen Sie die Installation:**

```bash
pip3.10 list  # Bei Option A
# ODER
pip list      # Bei Option B (mit aktiviertem venv)
```

Sie sollten Flask, SQLAlchemy, etc. sehen.

---

## 🗄️ Schritt 6: Datenbank initialisieren

```bash
cd ~/crm-system
# Falls Sie Option B gewählt haben:
# source venv/bin/activate

python3.10
```

In der Python-Shell:

```python
from app import create_app
from models import db

app = create_app()
with app.app_context():
    db.create_all()
    print("Datenbank erfolgreich erstellt!")

exit()
```

---

## 🌐 Schritt 7: Web App konfigurieren

1. Klicken Sie auf **"Web"** in der Navigation
2. Klicken Sie auf **"Add a new web app"**
3. Wählen Sie Ihren Domain-Namen: `IHR_USERNAME.pythonanywhere.com`
4. Klicken Sie **"Next"**
5. Wählen Sie **"Manual configuration"**
6. Wählen Sie **"Python 3.10"**
7. Klicken Sie **"Next"**

### Web App Details konfigurieren:

#### A. Source code Pfad:
```
/home/IHR_USERNAME/crm-system
```

#### B. Working directory:
```
/home/IHR_USERNAME/crm-system
```

#### C. Virtualenv:

**Falls Sie Option A gewählt haben (global):** Lassen Sie dieses Feld **LEER**

**Falls Sie Option B gewählt haben (venv):**
```
/home/IHR_USERNAME/crm-system/venv
```

#### D. WSGI Configuration File bearbeiten:

Klicken Sie auf den Link zur WSGI-Konfigurationsdatei (z.B. `/var/www/IHR_USERNAME_pythonanywhere_com_wsgi.py`)

**Löschen Sie den gesamten Inhalt** und ersetzen Sie ihn durch:

```python
import sys
import os
from dotenv import load_dotenv

# Pfad zu Ihrem Projekt
project_home = '/home/IHR_USERNAME/crm-system'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Lade Umgebungsvariablen
load_dotenv(os.path.join(project_home, '.env'))

# Importiere die Flask App
from app import create_app
application = create_app()
```

**Wichtig:** Ersetzen Sie `IHR_USERNAME` mit Ihrem tatsächlichen PythonAnywhere-Benutzernamen!

Speichern Sie die Datei (grüner "Save" Button).

---

## 🔄 Schritt 8: Statische Dateien konfigurieren

Scrollen Sie auf der Web-Seite nach unten zu **"Static files"**:

Fügen Sie zwei Einträge hinzu:

**1. Statische Dateien (CSS, JS, Bilder):**
- **URL:** `/static/`
- **Directory:** `/home/IHR_USERNAME/crm-system/crm_app/static/`

**2. Falls Sie Uploads haben (optional):**
- **URL:** `/uploads/`
- **Directory:** `/home/IHR_USERNAME/crm-system/uploads/`

---

## ✅ Schritt 9: Web App starten

1. Scrollen Sie auf der Web-Seite nach oben
2. Klicken Sie auf den grünen Button **"Reload IHR_USERNAME.pythonanywhere.com"**
3. Warten Sie ein paar Sekunden
4. Klicken Sie auf den Link zu Ihrer Website: `https://IHR_USERNAME.pythonanywhere.com`

🎉 **Ihre CRM-App sollte jetzt online sein!**

---

## 🧪 Schritt 10: Testdaten hinzufügen (optional)

Falls Sie Testdaten hinzufügen möchten:

```bash
cd ~/crm-system
# Falls Sie Option B (venv) gewählt haben:
# source venv/bin/activate

python3.10
```

```python
from app import create_app
from models import db, Customer, Order, Product, Contact, User
from datetime import datetime, timedelta
import random

app = create_app()

with app.app_context():
    # Beispiel: 5 Testkunden erstellen
    for i in range(1, 6):
        customer = Customer(
            first_name=f"Test{i}",
            last_name=f"Kunde{i}",
            email=f"test{i}@beispiel.at",
            phone=f"+43 664 {random.randint(1000000, 9999999)}"
        )
        db.session.add(customer)
    
    db.session.commit()
    print("Testdaten erfolgreich hinzugefügt!")

exit()
```

---

## 🐛 Fehlersuche (Troubleshooting)

### Problem: "Something went wrong" Fehler

**Lösung:**
1. Gehen Sie zu **"Web"** → **"Log files"**
2. Öffnen Sie das **Error log**
3. Lesen Sie die Fehlermeldung
4. Häufige Probleme:
   - Falsche Pfade im WSGI-File
   - Fehlende Pakete: `pip install -r requirements.txt` erneut ausführen
   - Falsche Python-Version: Verwenden Sie Python 3.10

### Problem: Statische Dateien (CSS) laden nicht

**Lösung:**
1. Überprüfen Sie die Static Files Konfiguration
2. Stellen Sie sicher, dass der Pfad korrekt ist
3. Reload der Web App

### Problem: Import-Fehler

**Lösung:**
```bash
cd ~/crm-system
# Falls Sie Option B (venv) gewählt haben:
# source venv/bin/activate

pip3.10 install --user --upgrade -r requirements.txt  # Bei Option A
# ODER
pip install --upgrade -r requirements.txt              # Bei Option B
```

### Problem: Datenbank-Fehler

**Lösung:**
```bash
cd ~/crm-system
rm crm.db  # Alte DB löschen
# Falls Sie Option B (venv) gewählt haben:
# source venv/bin/activate

python3.10
```

```python
from app import create_app
from models import db
app = create_app()
with app.app_context():
    db.create_all()
exit()
```

---

## 🔄 Updates deployen

Wenn Sie Änderungen am Code vornehmen:

### Mit Git:

```bash
# Lokal:
git add .
git commit -m "Beschreibung der Änderung"
git push

# Auf PythonAnywhere:
cd ~/crm-system
git pull
# Falls Sie Option B (venv) gewählt haben:
# source venv/bin/activate
# pip install -r requirements.txt  # Falls neue Pakete

# Bei Option A (global):
pip3.10 install --user -r requirements.txt  # Falls neue Pakete
```

Dann auf der Web-Seite auf **"Reload"** klicken!

### Ohne Git:

1. Laden Sie die geänderten Dateien über "Files" hoch
2. Klicken Sie auf **"Reload"** auf der Web-Seite

---

## 📊 Logs anzeigen

**Error Log:**
```
Web → Log files → Error log
```

**Server Log:**
```
Web → Log files → Server log
```

**Access Log:**
```
Web → Log files → Access log
```

---

## ⚡ Performance-Tipps

1. **Kostenloser Account Limits:**
   - CPU-Zeit: Begrenzt
   - Wird täglich um 00:00 UTC zurückgesetzt
   - Website schläft nach Inaktivität (wacht bei Zugriff auf)

2. **Upgrade-Optionen:**
   - Für permanente Verfügbarkeit: Hacker Plan ($5/Monat)
   - Mehr CPU und kein Schlafmodus

3. **Optimierungen:**
   - Caching verwenden
   - Datenbankabfragen optimieren
   - Statische Dateien komprimieren

---

## 🔒 Sicherheit

**Wichtig für Produktion:**

1. **Ändern Sie den SECRET_KEY:**
   ```python
   import secrets
   secrets.token_hex(32)
   ```

2. **Aktivieren Sie HTTPS** (automatisch bei PythonAnywhere)

3. **Niemals `.env` oder Credentials committen**
   - Fügen Sie `.env` zur `.gitignore` hinzu:
   ```bash
   echo ".env" >> .gitignore
   echo "*.db" >> .gitignore
   echo "__pycache__/" >> .gitignore
   echo "venv/" >> .gitignore
   ```

4. **Datensicherung:**
   ```bash
   # Datenbank sichern
   cd ~/crm-system
   cp crm.db crm_backup_$(date +%Y%m%d).db
   ```

---

## 📱 Zugriff auf Ihre App

Nach erfolgreichem Deployment:

**URL:** `https://IHR_USERNAME.pythonanywhere.com`

Teilen Sie diese URL mit Ihren Lehrern oder Mitschülern!

---

## ❓ Häufig gestellte Fragen (FAQ)

**Q: Kann ich eine eigene Domain verwenden?**
A: Ja, aber nur mit einem bezahlten Plan (ab $5/Monat)

**Q: Wie lange bleiben meine Daten gespeichert?**
A: Für immer, solange Ihr Account aktiv ist

**Q: Kann ich die Datenbank exportieren?**
A: Ja, über "Files" können Sie `crm.db` herunterladen

**Q: Was passiert bei zu viel Traffic?**
A: Kostenloser Account: Website wird langsamer. Upgrade empfohlen.

**Q: Gibt es Backups?**
A: Nein, erstellen Sie regelmäßig eigene Backups!

---

## 📞 Support

**PythonAnywhere Help:**
- Forum: https://www.pythonanywhere.com/forums/
- Help Pages: https://help.pythonanywhere.com/

**Bei Problemen:**
1. Überprüfen Sie die Error Logs
2. Suchen Sie im PythonAnywhere Forum
3. Fragen Sie Ihren Lehrer/Ihre Lehrerin

---

## ✅ Checkliste vor der Abgabe

- [ ] App läuft ohne Fehler
- [ ] Alle Seiten erreichbar (Dashboard, Kunden, Bestellungen, Kontakte)
- [ ] Testdaten eingegeben
- [ ] CSS und Design funktioniert
- [ ] CRUD-Operationen testen (Create, Read, Update, Delete)
- [ ] URL notiert für Abgabe
- [ ] Screenshots gemacht (optional)
- [ ] Datenbank gesichert

---

## 🎓 Für die Projektdokumentation

Fügen Sie folgende Informationen zu Ihrer Dokumentation hinzu:

**Deployment-Details:**
- Platform: PythonAnywhere
- URL: https://IHR_USERNAME.pythonanywhere.com
- Python-Version: 3.10
- Framework: Flask 3.0.0
- Datenbank: SQLite
- Hosting-Typ: Cloud-basiert (kostenlos)

**Technologie-Stack:**
- Backend: Flask + SQLAlchemy
- Frontend: Bootstrap 5 + Jinja2
- Deployment: PythonAnywhere WSGI
- Version Control: Git/GitHub (optional)

---

Viel Erfolg mit Ihrem Deployment! 🚀

Bei Fragen oder Problemen: Überprüfen Sie die Error Logs und folgen Sie der Troubleshooting-Sektion.
