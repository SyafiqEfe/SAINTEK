import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///masjid.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload configurations
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Remember to create these folders
    os.makedirs(os.path.join(UPLOAD_FOLDER, 'gallery'), exist_ok=True)
    os.makedirs(os.path.join(UPLOAD_FOLDER, 'articles'), exist_ok=True)
    os.makedirs(os.path.join(UPLOAD_FOLDER, 'lectures'), exist_ok=True)