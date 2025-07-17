# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# from flask_login import LoginManager # Marked for removal/commenting

db = SQLAlchemy()
migrate = Migrate()

# login_manager = LoginManager() # Marked for removal/commenting
# login_manager.login_view = 'auth.login' # Marked for removal/commenting
# login_manager.login_message = 'Please log in to access this page.' # Marked for removal/commenting
# login_manager.login_message_category = 'info' # Marked for removal/commenting
