import os

# Główny katalog projektu
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Dedykowany katalog na pliki instancji (np. baza danych), poza pakietem aplikacji
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')

# AUTOMATYZACJA: Jeśli folder nie istnieje, Python stworzy go sam przy starcie
os.makedirs(INSTANCE_DIR, exist_ok=True)

class Config:
    # Pobierz klucz z .env, jeśli go brak - użyj bezpiecznego fallbacku dla dev
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-default-foolproof-key')

    # Baza danych zawsze ląduje w automatycznie stworzonym folderze instance
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(INSTANCE_DIR, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
