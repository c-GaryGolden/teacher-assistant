from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from app import db
from app.models import User, SchoolClass, ProjectGroup
from app.decorators import teacher_required

school_bp = Blueprint('school', __name__)

# --- KLASY ---

@school_bp.route('/create_class', methods=['GET', 'POST'])
@login_required
def create_class():
    if request.method == 'POST':
        name = request.form.get('name') # 'name' musi zgadzać się z field.name w szablonie
        if not name:
            return "Błąd: Nazwa jest wymagana!", 400
        new_class = SchoolClass(name=name)
        db.session.add(new_class)
        db.session.commit() # Tu wywalało błąd, bo name było None
        return redirect(url_for('dashboard.index'))
    
    fields = [{'name': 'name', 'type': 'text', 'placeholder': 'Nazwa klasy'}]
    return render_template('form_layout.html', title='Stwórz klasę', fields=fields, btn_text='Zapisz')

@school_bp.route('/join_class/<int:class_id>')
@login_required
def join_class(class_id):
    school_class = SchoolClass.query.get_or_404(class_id)
    if current_user not in school_class.students:
        school_class.students.append(current_user)
        db.session.commit()
    return redirect(url_for('dashboard.index'))

@school_bp.route('/delete_class/<int:class_id>')
@login_required
@teacher_required
def delete_class(class_id):
    obj = SchoolClass.query.get_or_404(class_id)
    db.session.delete(obj)
    db.session.commit()
    return redirect(url_for('dashboard.index'))

# --- GRUPY ---

# app/routes/school.py

@school_bp.route('/create_group', methods=['GET', 'POST'])
@login_required
@teacher_required # Zakładając, że masz taki dekorator
def create_group():
    if request.method == 'POST':
        group_name = request.form.get('name') # MUSI być 'name'
        if not group_name:
            return "Błąd: Nazwa grupy nie może być pusta!", 400
            
        new_group = ProjectGroup(
            name=group_name,
            description=request.form.get('description')
        )
        db.session.add(new_group)
        db.session.commit()
        return redirect(url_for('dashboard.index'))

    # To są dane przesyłane do form_layout.html
    fields = [
        {'name': 'name', 'type': 'text', 'placeholder': 'Nazwa grupy'},
        {'name': 'description', 'type': 'textarea', 'placeholder': 'Opis projektu'}
    ]
    return render_template('form_layout.html', title="Nowa Grupa", fields=fields, btn_text="Stwórz Grupę")

@school_bp.route('/join_group/<int:group_id>')
@login_required
def join_group(group_id):
    group = ProjectGroup.query.get_or_404(group_id)
    if current_user not in group.members:
        group.members.append(current_user)
        db.session.commit()
    return redirect(url_for('dashboard.index'))

@school_bp.route('/leave_group/<int:group_id>')
@login_required
def leave_group(group_id):
    group = ProjectGroup.query.get_or_404(group_id)
    if current_user in group.members:
        group.members.remove(current_user)
        db.session.commit()
    return redirect(url_for('dashboard.index'))

@school_bp.route('/delete_group/<int:group_id>')
@login_required
@teacher_required
def delete_group(group_id):
    obj = ProjectGroup.query.get_or_404(group_id)
    db.session.delete(obj)
    db.session.commit()
    return redirect(url_for('dashboard.index'))

# --- SYSTEM POMOCY ---

@school_bp.route('/request_help')
@login_required
def request_help():
    if current_user.role == 'student':
        current_user.needs_help = not current_user.needs_help
        db.session.commit()
    return redirect(url_for('dashboard.index'))

@school_bp.route('/group_help/<int:group_id>')
@login_required
def group_help(group_id):
    group = ProjectGroup.query.get_or_404(group_id)
    if current_user in group.members:
        group.needs_help = not group.needs_help
        db.session.commit()
    return redirect(url_for('dashboard.index'))
