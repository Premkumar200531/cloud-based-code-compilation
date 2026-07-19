
from datetime import datetime, timezone
from database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user')
    is_active = db.Column(db.Boolean, default=True) # For managing user behavior (enable/disable)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    logs = db.relationship('UserLog', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class UserLog(db.Model):
    __tablename__ = 'user_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    login_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    logout_at = db.Column(db.DateTime, nullable=True)

class Language(db.Model):
    __tablename__ = 'languages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    version = db.Column(db.String(20))
    compile_cmd = db.Column(db.String(200)) # e.g., 'gcc {file} -o {out}'
    run_cmd = db.Column(db.String(200), nullable=False) # e.g., './{out}' or 'python {file}'
    is_active = db.Column(db.Boolean, default=True)

class Run(db.Model):
    __tablename__ = 'runs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # Can be anonymous
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=False)
    code = db.Column(db.Text, nullable=False)
    stdin = db.Column(db.Text)
    stdout = db.Column(db.Text)
    stderr = db.Column(db.Text)
    status = db.Column(db.String(20)) # success, error, timeout
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    time_ms = db.Column(db.Integer)

class Problem(db.Model):
    __tablename__ = 'problems'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20), default='easy')
    testcases = db.relationship('TestCase', backref='problem', lazy=True)

class TestCase(db.Model):
    __tablename__ = 'testcases'
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'), nullable=False)
    input_data = db.Column(db.Text, nullable=False)
    expected_output = db.Column(db.Text, nullable=False)
    is_hidden = db.Column(db.Boolean, default=False)

class Snippet(db.Model):
    __tablename__ = 'snippets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=True) # Null for playground
    title = db.Column(db.String(100), nullable=False)
    code = db.Column(db.Text, nullable=False) # For playground, this can be a JSON string
    is_playground = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', backref='snippets')
    language = db.relationship('Language', backref='snippets')

from datetime import datetime, timezone
from database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user')
    is_active = db.Column(db.Boolean, default=True) # For managing user behavior (enable/disable)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    logs = db.relationship('UserLog', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class UserLog(db.Model):
    __tablename__ = 'user_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    login_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    logout_at = db.Column(db.DateTime, nullable=True)

class Language(db.Model):
    __tablename__ = 'languages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    version = db.Column(db.String(20))
    compile_cmd = db.Column(db.String(200)) # e.g., 'gcc {file} -o {out}'
    run_cmd = db.Column(db.String(200), nullable=False) # e.g., './{out}' or 'python {file}'
    is_active = db.Column(db.Boolean, default=True)

class Run(db.Model):
    __tablename__ = 'runs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # Can be anonymous
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=False)
    code = db.Column(db.Text, nullable=False)
    stdin = db.Column(db.Text)
    stdout = db.Column(db.Text)
    stderr = db.Column(db.Text)
    status = db.Column(db.String(20)) # success, error, timeout
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    time_ms = db.Column(db.Integer)

class Problem(db.Model):
    __tablename__ = 'problems'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20), default='easy')
    testcases = db.relationship('TestCase', backref='problem', lazy=True)

class TestCase(db.Model):
    __tablename__ = 'testcases'
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'), nullable=False)
    input_data = db.Column(db.Text, nullable=False)
    expected_output = db.Column(db.Text, nullable=False)
    is_hidden = db.Column(db.Boolean, default=False)

class Snippet(db.Model):
    __tablename__ = 'snippets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=True) # Null for playground
    title = db.Column(db.String(100), nullable=False)
    code = db.Column(db.Text, nullable=False) # For playground, this can be a JSON string
    is_playground = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', backref='snippets')
    language = db.relationship('Language', backref='snippets')

