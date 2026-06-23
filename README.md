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
## 🛠️ Stack Technologiczny

| Warstwa | Wybrana technologia | Rola w aplikacji / Charakterystyka |
| :--- | :--- | :--- |
| **Backend** | Python 3.12 + Flask 3.1 | Główny motor aplikacji. Obsługuje routing, logikę biznesową, autoryzację i przetwarzanie plików. |
| **Frontend** | Pico CSS + Jinja2 | Pico CSS to ultralekki framework CSS, który automatycznie styluje czyste, semantyczne tagi HTML (formularze, tabele, przyciski) bez używania skomplikowanych klas. Jinja2 odpowiada za dynamiczne wstrzykiwanie danych z Pythona do szablonów. |
| **Baza danych** | SQLAlchemy ORM + SQLite | Mapowanie obiektowo-relacyjne (brak czystego SQL w kodzie). SQLite przechowuje dane w jednym pliku lokalnym. Tabele są generowane automatycznie przy starcie aplikacji przez `db.create_all()`. |
| **Autentykacja** | Flask-Login | Obsługa ciasteczek sesyjnych, bezpieczne logowanie oraz ochrona tras przed nieuprawnionym dostępem za pomocą dekoratorów. |
