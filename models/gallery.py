from extensions import db
from datetime import datetime

class GalleryCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    images = db.relationship('GalleryImage', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<GalleryCategory {self.name}>'

class GalleryImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(255), nullable=False)
    event_date = db.Column(db.Date, nullable=True)
    
    category_id = db.Column(db.Integer, db.ForeignKey('gallery_category.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<GalleryImage {self.title}>'