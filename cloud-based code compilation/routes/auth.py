<<<<<<< HEAD
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from models import User, UserLog
from database import db
from datetime import datetime, timezone

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('Please check your login details and try again.', 'danger')
            return redirect(url_for('auth.login'))
        
        if not user.is_active:
            flash('Your account has been disabled by an administrator.', 'warning')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        
        # Log login
        log = UserLog(user_id=user.id)
        db.session.add(log)
        db.session.commit()
        
        return redirect(url_for('main.dashboard'))

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('name') # Form field might still be named 'name'
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email address already exists', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(email=email, username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        
        # Log initial login
        log = UserLog(user_id=new_user.id)
        db.session.add(log)
        db.session.commit()
        
        return redirect(url_for('main.dashboard'))

    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    # Log logout time for the last active log entry
    last_log = UserLog.query.filter_by(user_id=current_user.id, logout_at=None).order_by(UserLog.login_at.desc()).first()
    if last_log:
        last_log.logout_at = datetime.now(timezone.utc)
        db.session.commit()
        
    logout_user()
    return redirect(url_for('main.index'))
=======
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from models import User, UserLog
from database import db
from datetime import datetime, timezone

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('Please check your login details and try again.', 'danger')
            return redirect(url_for('auth.login'))
        
        if not user.is_active:
            flash('Your account has been disabled by an administrator.', 'warning')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        
        # Log login
        log = UserLog(user_id=user.id)
        db.session.add(log)
        db.session.commit()
        
        return redirect(url_for('main.dashboard'))

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('name') # Form field might still be named 'name'
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email address already exists', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(email=email, username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        
        # Log initial login
        log = UserLog(user_id=new_user.id)
        db.session.add(log)
        db.session.commit()
        
        return redirect(url_for('main.dashboard'))

    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    # Log logout time for the last active log entry
    last_log = UserLog.query.filter_by(user_id=current_user.id, logout_at=None).order_by(UserLog.login_at.desc()).first()
    if last_log:
        last_log.logout_at = datetime.now(timezone.utc)
        db.session.commit()
        
    logout_user()
    return redirect(url_for('main.index'))
>>>>>>> 1b9f44e803ada8be2eab82c14e451e7713b058b2
