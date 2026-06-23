import os
from flask import Blueprint, render_template, request, redirect, url_for, send_file, abort, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import Repository, File, AssignmentSubmission, SchoolClass, ProjectGroup, User
from app.decorators import teacher_required

repo_bp = Blueprint('repo', __name__)

# --- ZARZĄDZANIE REPOZYTORIAMI ---

@repo_bp.route('/repository/new', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.role != 'teacher': abort(403)
    
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            return "Błąd: Nazwa repozytorium jest wymagana!", 400
            
        new_repo = Repository(
            name=name,
            description=request.form.get('description'),
            owner_id=current_user.id
        )
        db.session.add(new_repo)
        db.session.commit()
        return redirect(url_for('dashboard.index'))
    
    # TEGO BRAKOWAŁO:
    fields = [
        {'name': 'name', 'type': 'text', 'placeholder': 'Nazwa repozytorium'},
        {'name': 'description', 'type': 'textarea', 'placeholder': 'Opis (opcjonalnie)'}
    ]
    
    return render_template('form_layout.html', 
                           title="Nowe Repozytorium", 
                           fields=fields, 
                           btn_text="Utwórz repozytorium")
@repo_bp.route('/assign_repository/<int:repo_id>', methods=['GET', 'POST'])
@login_required
@teacher_required
def assign(repo_id):
    repo = Repository.query.get_or_404(repo_id)
    
    if request.method == 'POST':
        class_id = request.form.get('class_id')
        group_id = request.form.get('group_id')
        user_id = request.form.get('user_id')
        
        repo.assigned_class_id = int(class_id) if class_id else None
        repo.assigned_group_id = int(group_id) if group_id else None
        repo.assigned_user_id = int(user_id) if user_id else None
        
        # POPRAWKA LOGICZNA: Jeśli przypisano jakiekolwiek restrykcje, repozytorium przestaje być publiczne
        if repo.assigned_class_id or repo.assigned_group_id or repo.assigned_user_id:
            repo.is_public = False
        else:
            repo.is_public = True
            
        db.session.commit()
        return redirect(url_for('dashboard.index'))
    
    fields = [
        {
            'name': 'class_id', 
            'type': 'select', 
            'placeholder': 'Przypisz do klasy', 
            'options': SchoolClass.query.all(),
            'value': repo.assigned_class_id
        },
        {
            'name': 'group_id', 
            'type': 'select', 
            'placeholder': 'Przypisz do grupy', 
            'options': ProjectGroup.query.all(),
            'value': repo.assigned_group_id
        },
        {
            'name': 'user_id', 
            'type': 'select', 
            'placeholder': 'Przypisz do studenta', 
            'options': User.query.filter_by(role='student').all(),
            'value': repo.assigned_user_id
        }
    ]
    
    return render_template('form_layout.html', 
                           title=f"Uprawnienia: {repo.name}", 
                           fields=fields, 
                           btn_text="Aktualizuj uprawnienia")
# --- OBSŁUGA PLIKÓW (UPLOAD/DOWNLOAD) ---

@repo_bp.route('/upload_file/<int:repo_id>', methods=['GET', 'POST'])
@login_required
@teacher_required
def upload(repo_id):
    repo = Repository.query.get_or_404(repo_id)
    
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.root_path, 'uploads', filename)
            file.save(upload_path)
            
            new_file = File(filename=filename, stored_path=f'uploads/{filename}', repository_id=repo.id)
            db.session.add(new_file)
            db.session.commit()
        return redirect(url_for('dashboard.index'))
    
    # Naprawione: zmienna zdefiniowana poza blokiem POST, dostępna dla żądania GET
    fields = [
        {'name': 'file', 'placeholder': 'Wybierz plik z komputera', 'type': 'file'}
    ]
    
    return render_template('form_layout.html', 
                           title="Wgraj plik", 
                           fields=fields, 
                           btn_text="Wgraj plik")

@repo_bp.route('/download/<int:file_id>')
@login_required
def download(file_id):
    f = File.query.get_or_404(file_id)
    return send_file(os.path.join(current_app.root_path, f.stored_path), as_attachment=True)

# --- ZADANIA DOMOWE (SUBMISSIONS) ---

@repo_bp.route('/submit_assignment/<int:repo_id>', methods=['GET', 'POST'])
@login_required
def submit(repo_id):
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            # Twoja obecna logika zapisu pliku...
            filename = f"sub_{current_user.id}_{secure_filename(file.filename)}"
            path = os.path.join('submissions', filename)
            file.save(os.path.join(current_app.root_path, path))
            
            sub = AssignmentSubmission(student_id=current_user.id, repository_id=repo_id, file_path=path)
            db.session.add(sub)
            db.session.commit()
            return redirect(url_for('dashboard.index'))
    
    # DODAJ TO, aby pole wyboru pliku się pojawiło:
    fields = [
        {
            'name': 'file', 
            'type': 'file', 
            'placeholder': 'Wybierz plik z rozwiązaniem'
        }
    ]
    
    return render_template('form_layout.html', 
                           title="Odeślij zadanie", 
                           fields=fields, 
                           btn_text="Wyślij rozwiązanie")

@repo_bp.route('/view_submissions')
@login_required
@teacher_required
def view_all_submissions():
    subs = AssignmentSubmission.query.order_by(AssignmentSubmission.timestamp.desc()).all()
    return render_template('submissions.html', submissions=subs)

@repo_bp.route('/download_submission/<int:submission_id>')
@login_required
@teacher_required
def download_submission(submission_id):
    sub = AssignmentSubmission.query.get_or_404(submission_id)
    # Zwróć uwagę, że path musi być poprawną ścieżką do folderu submissions
    return send_file(os.path.join(current_app.root_path, sub.file_path), as_attachment=True)
    
@repo_bp.route('/delete_repository/<int:repo_id>', methods=['POST'])
@login_required
@teacher_required
def delete(repo_id):
    repo = Repository.query.get_or_404(repo_id)
    
    # Usuwanie rekordów z bazy danych
    db.session.delete(repo)
    db.session.commit()
    
    # Powrót do dashboardu po usunięciu
    return redirect(url_for('dashboard.index'))    
