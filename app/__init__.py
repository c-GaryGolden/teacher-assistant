from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # --- REJESTRACJA MODUŁÓW (BLUEPRINTÓW) ---
    # WAŻNE: Wszystkie importy i register_blueprint muszą mieć dokładnie 4 spacje wcięcia!
    
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.routes.school import school_bp
    app.register_blueprint(school_bp)

    from app.routes.repository import repo_bp
    app.register_blueprint(repo_bp)

    # Czat zarejestrujemy w następnym kroku, na razie zostawiam zakomentowany
    from app.routes.chat import chat_bp
    app.register_blueprint(chat_bp)

    with app.app_context():
        db.create_all()

    return app
