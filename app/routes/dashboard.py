from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import User, SchoolClass, ProjectGroup, Repository

# TA LINIA JEST KLUCZOWA - nazwa musi być 'dashboard_bp'
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    if current_user.role == 'teacher':
        repos = Repository.query.all()
        help_alerts = {
            'students': User.query.filter_by(role='student', needs_help=True).all(),
            'groups': ProjectGroup.query.filter_by(needs_help=True).all()
        }
    else:
        repos = Repository.query.filter(
            (Repository.is_public == True) |
            (Repository.assigned_class_id.in_([c.id for c in current_user.classes])) |
            (Repository.assigned_group_id.in_([g.id for g in current_user.groups])) |
            (Repository.assigned_user_id == current_user.id)
        ).all()
        help_alerts = None

    return render_template('dashboard.html', 
                           user=current_user, 
                           repositories=repos, 
                           help_alerts=help_alerts,
                           classes=SchoolClass.query.all(), 
                           groups=ProjectGroup.query.all())
