<<<<<<< HEAD
from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/editor')
def editor():
    return render_template('editor.html')

@main.route('/playground')
def playground():
    return render_template('playground.html')

@main.route('/dashboard')
@login_required
def dashboard():
    from models import Run
    runs = Run.query.filter_by(user_id=current_user.id).order_by(Run.created_at.desc()).limit(10).all()
    return render_template('dashboard.html', name=current_user.username, runs=runs)
=======
from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/editor')
def editor():
    return render_template('editor.html')

@main.route('/playground')
def playground():
    return render_template('playground.html')

@main.route('/dashboard')
@login_required
def dashboard():
    from models import Run
    runs = Run.query.filter_by(user_id=current_user.id).order_by(Run.created_at.desc()).limit(10).all()
    return render_template('dashboard.html', name=current_user.username, runs=runs)
>>>>>>> 1b9f44e803ada8be2eab82c14e451e7713b058b2
