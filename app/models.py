from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Tabele łączące (Many-to-Many)
class_members = db.Table('class_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('class_id', db.Integer, db.ForeignKey('school_class.id'))
)

group_members = db.Table('group_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('project_group.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'teacher' lub 'student'
    needs_help = db.Column(db.Boolean, default=False)

    classes = db.relationship('SchoolClass', secondary=class_members, back_populates='students')
    groups = db.relationship('ProjectGroup', secondary=group_members, back_populates='members')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class SchoolClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    students = db.relationship('User', secondary=class_members, back_populates='classes')
    repositories = db.relationship('Repository', backref='assigned_class', lazy=True)

class ProjectGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    needs_help = db.Column(db.Boolean, default=False)
    members = db.relationship('User', secondary=group_members, back_populates='groups')
    repositories = db.relationship('Repository', backref='assigned_group', lazy=True)

class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=True)
    password_hash = db.Column(db.String(255), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # SYSTEM UPRAWNIEŃ
    assigned_class_id = db.Column(db.Integer, db.ForeignKey('school_class.id'), nullable=True)
    assigned_group_id = db.Column(db.Integer, db.ForeignKey('project_group.id'), nullable=True)
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    files = db.relationship('File', backref='repository', lazy=True, cascade="all, delete-orphan")

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    stored_path = db.Column(db.String(500), nullable=False)
    repository_id = db.Column(db.Integer, db.ForeignKey('repository.id'))
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'))

class AssignmentSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    repository_id = db.Column(db.Integer, db.ForeignKey('repository.id'))
    file_path = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())
    student = db.relationship('User', backref='submissions')
    repository = db.relationship('Repository', backref='submissions')
    repository_id = db.Column(db.Integer, db.ForeignKey('repository.id'), nullable=False)
    repository = db.relationship('Repository', backref=db.backref('submissions', cascade="all, delete-orphan"))
class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    author = db.relationship('User', foreign_keys=[author_id], backref='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages')
