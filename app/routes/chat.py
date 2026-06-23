from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import User, ChatMessage
from sqlalchemy import or_

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chats')
@login_required
def chat_list():
    # Pobieramy listę wszystkich użytkowników (oprócz nas samych), z którymi możemy pisać
    users = User.query.filter(User.id != current_user.id).all()
    return render_template('chat_list.html', users=users)

@chat_bp.route('/chat/<int:recipient_id>', methods=['GET', 'POST'])
@login_required
def chat(recipient_id):
    recipient = User.query.get_or_404(recipient_id)
    
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            msg = ChatMessage(content=content, author_id=current_user.id, recipient_id=recipient_id)
            db.session.add(msg)
            db.session.commit()
        return redirect(url_for('chat.chat', recipient_id=recipient_id))

    # Pobieramy historię rozmowy między zalogowanym a wybranym użytkownikiem
    messages = ChatMessage.query.filter(
        or_(
            (ChatMessage.author_id == current_user.id) & (ChatMessage.recipient_id == recipient_id),
            (ChatMessage.author_id == recipient_id) & (ChatMessage.recipient_id == current_user.id)
        )
    ).order_by(ChatMessage.timestamp.asc()).all()

    return render_template('chat.html', recipient=recipient, messages=messages)
