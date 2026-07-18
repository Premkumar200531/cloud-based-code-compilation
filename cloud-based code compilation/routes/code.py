from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import Language, Run, Snippet
from database import db
from services.runner import CodeRunner

code_bp = Blueprint('code', __name__)

@code_bp.route('/execute', methods=['POST'])
def execute_code():
    data = request.get_json()
    language_id = data.get('language_id')
    source_code = data.get('code')
    stdin = data.get('stdin', '')

    lang = Language.query.get(language_id)
    if not lang:
        return jsonify({'error': 'Language not supported'}), 400

    # Ensure command formats are correct in DB or generic runner
    # For MVP, we might hardcode commands in runner service if DB is empty or just pass lang object
    
    result = CodeRunner.run_code(lang, source_code, stdin)
    
    # Log the run
    new_run = Run(
        user_id=current_user.id if current_user.is_authenticated else None,
        language_id=language_id,
        code=source_code,
        stdin=stdin,
        stdout=result.get('stdout'),
        stderr=result.get('stderr'),
        status=result.get('status'),
        time_ms=result.get('time_ms')
    )
    db.session.add(new_run)
    db.session.commit()

    return jsonify(result)

@code_bp.route('/languages', methods=['GET'])
def get_languages():
    langs = Language.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': l.id,
        'name': l.name,
        'version': l.version
    } for l in langs])

@code_bp.route('/snippets/save', methods=['POST'])
@login_required
def save_snippet():
    data = request.get_json()
    title = data.get('title', 'Untitled')
    code = data.get('code')
    language_id = data.get('language_id')
    if language_id == '':
        language_id = None
        
    is_playground = data.get('is_playground', False)

    snippet = Snippet(
        user_id=current_user.id,
        title=title,
        code=code,
        language_id=language_id,
        is_playground=is_playground
    )
    db.session.add(snippet)
    db.session.commit()
    return jsonify({'message': 'Snippet saved successfully', 'id': snippet.id})

@code_bp.route('/snippets', methods=['GET'])
@login_required
def list_snippets():
    snippets = Snippet.query.filter_by(user_id=current_user.id).order_by(Snippet.created_at.desc()).all()
    return jsonify([{
        'id': s.id,
        'title': s.title,
        'language': s.language.name if s.language else 'Web',
        'is_playground': s.is_playground,
        'created_at': s.created_at.strftime('%Y-%m-%d %H:%M')
    } for s in snippets])

@code_bp.route('/snippet/<int:snippet_id>', methods=['GET'])
@login_required
def get_snippet(snippet_id):
    snippet = Snippet.query.filter_by(id=snippet_id, user_id=current_user.id).first_or_404()
    return jsonify({
        'title': snippet.title,
        'code': snippet.code,
        'language_id': snippet.language_id,
        'is_playground': snippet.is_playground
    })
