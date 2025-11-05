"""
WSGI Entry Point für PythonAnywhere Deployment
"""

import sys
import os

# Füge das Projektverzeichnis zum Python-Pfad hinzu
project_home = '/home/yourusername/Projekt_CRM'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Importiere die Flask-App
from app import create_app

application = create_app()

if __name__ == "__main__":
    application.run()
