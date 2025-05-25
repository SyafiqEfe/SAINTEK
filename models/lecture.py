from extensions import db
from datetime import datetime

class LectureCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    lectures = db.relationship('Lecture', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<LectureCategory {self.name}>'

class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=True)  # in minutes
    location = db.Column(db.String(200), nullable=True)
    speaker = db.Column(db.String(100), nullable=True)
    youtube_link = db.Column(db.String(255), nullable=True)
    materials_file = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    
    category_id = db.Column(db.Integer, db.ForeignKey('lecture_category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Lecture {self.title}>'