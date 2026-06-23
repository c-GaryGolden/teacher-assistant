# 🧑‍🏫 Teacher Assistant

Teacher Assistant to aplikacja webowa stworzona w celu ułatwienia codziennej pracy nauczycielom i kadrze dydaktycznej. System pozwala na zarządzanie strukturą szkoły, repozytorium materiałów oraz oferuje moduły komunikacyjne, automatyzując powtarzalne zadania i porządkując dokumentację.

---

## 🚀 Kluczowe funkcje

Aplikacja jest podzielona na dedykowane moduły:
* 🔐 **Autoryzacja (Auth):** Bezpieczny system rejestracji i logowania użytkowników (nauczycieli) oparty na `Flask-Login`.
* 📊 **Panel Główny (Dashboard):** Centralne miejsce z podsumowaniem najważniejszych informacji i statystyk.
* 🏫 **Zarządzanie Szkołą (School):** Moduł do organizacji struktury klas, uczniów oraz zajęć.
* 📁 **Repozytorium (Repository):** Przestrzeń na materiały dydaktyczne, konspekty lekcji i pliki przesyłane przez nauczyciela.
* 💬 **Czat (Chat):** Wbudowany system komunikacji ułatwiający wymianę informacji.

---

teacher-assistant/
├── app/                    # Pakiet główny aplikacji
│   ├── routes/             # Logika poszczególnych modułów
│   │   ├── auth.py
│   │   ├── chat.py
│   │   ├── dashboard.py
│   │   ├── repository.py
│   │   └── school.py
│   ├── submissions/        # [Lokalny / Ignorowany] Folder na zadania domowe uczniów
│   ├── templates/          # Szablony HTML (Jinja2)
│   ├── uploads/            # [Lokalny / Ignorowany] Folder na materiały dydaktyczne
│   ├── __init__.py         # Inicjalizacja aplikacji i rejestracja modułów
│   ├── decorators.py       # Dekoratory uprawnień i dostępu
│   └── models.py           # Struktura tabel bazy danych (SQLAlchemy)
├── instance/               # [Automatycznie generowany] Katalog na dane aplikacji
│   └── app.db              # Lokalny plik bazy danych SQLite
├── config.py               # Automatyzacja tworzenia środowiska i parametrów aplikacji
├── requirements.txt        # Zablokowane wersje bibliotek
└── run.py                  # Główny punkt startowy aplikacji
