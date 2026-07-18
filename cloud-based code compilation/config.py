<<<<<<< HEAD
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///online_compiler.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Execution constraints
    EXECUTION_TIMEOUT = 5  # seconds
    MAX_MEMORY = 512 * 1024 * 1024  # 512 MB (in bytes, simpler for python runner)
=======
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///online_compiler.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Execution constraints
    EXECUTION_TIMEOUT = 5  # seconds
    MAX_MEMORY = 512 * 1024 * 1024  # 512 MB (in bytes, simpler for python runner)
>>>>>>> 1b9f44e803ada8be2eab82c14e451e7713b058b2
