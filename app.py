from flask import Flask, session, flash
from config import Config
from extensions import db
from routes.main_routes import main_bp
from routes.admin_routes import admin_bp
from routes.lecture_routes import lecture_bp
from routes.article_routes import article_bp
from routes.gallery_routes import gallery_bp
from routes.cashflow_routes import cashflow_bp
from datetime import datetime
import os # Pastikan os diimpor

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)

  print(f"DEBUG: SQLALCHEMY_DATABASE_URI = {app.config.get('SQLALCHEMY_DATABASE_URI')}")

  # Initialize extensions
  db.init_app(app)

  # --- TAMBAHKAN BARIS INI DI SINI UNTUK MEMBUAT FOLDER ---
  # Pastikan UPLOAD_FOLDER sudah didefinisikan di config
  upload_folder_base = app.config['UPLOAD_FOLDER']
  os.makedirs(os.path.join(upload_folder_base, 'gallery'), exist_ok=True)
  os.makedirs(os.path.join(upload_folder_base, 'articles'), exist_ok=True)
  os.makedirs(os.path.join(upload_folder_base, 'lectures'), exist_ok=True)
  # -------------------------------------------------------

  # Global context: inject 'now' into all templates
  @app.context_processor
  def inject_now():
      return {'now': datetime.now()}
  # Register blueprints
  app.register_blueprint(main_bp)
  app.register_blueprint(admin_bp, url_prefix='/admin')
  app.register_blueprint(lecture_bp, url_prefix='/lectures')
  app.register_blueprint(article_bp, url_prefix='/articles')
  app.register_blueprint(gallery_bp, url_prefix='/gallery')
  app.register_blueprint(cashflow_bp, url_prefix='/')

  # Create database tables
  with app.app_context():
      db.create_all()

  return app

if __name__ == '__main__':
  app = create_app()
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
