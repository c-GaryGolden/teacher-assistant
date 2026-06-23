from functools import wraps
from flask import abort
from flask_login import current_user

def teacher_required(f):
    """
    Dekorator sprawdzający, czy zalogowany użytkownik ma rolę nauczyciela.
    Jeśli nie, natychmiast zwraca błąd 403 (Brak dostępu).
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'teacher':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
