import os

# Główny katalog projektu
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# 1. Automatyzacja dla bazy danych (katalog instance)
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
os.makedirs(INSTANCE_DIR, exist_ok=True)

# 2. AUTOMATYZACJA DLA UPLOADU: Automatyczne tworzenie folderu na zadania uczniów
SUBMISSIONS_DIR = os.path.join(BASE_DIR, 'app', 'submissions')
os.makedirs(SUBMISSIONS_DIR, exist_ok=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-default-foolproof-key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(INSTANCE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Dobra praktyka: wystawienie ścieżki do konfiguracji Flaska
    UPLOAD_FOLDER = SUBMISSIONS_DIR
