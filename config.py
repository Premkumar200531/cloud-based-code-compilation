import os

def _db_url():
    url = os.environ.get('DATABASE_URL') or 'sqlite:///online_compiler.db'
    # Render/Heroku give postgres://, SQLAlchemy 2 needs postgresql://
    if url.startswith('postgres://'):
        url = url.replace('postgres://', 'postgresql://', 1)
    return url

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    SQLALCHEMY_DATABASE_URI = _db_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Execution constraints
    EXECUTION_TIMEOUT = 5  # seconds
    MAX_MEMORY = 512 * 1024 * 1024  # 512 MB
