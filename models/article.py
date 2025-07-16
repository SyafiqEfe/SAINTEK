from extensions import db
from datetime import datetime

class ArticleCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    articles = db.relationship('Article', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<ArticleCategory {self.name}>'

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=True)

    category_id = db.Column(db.Integer, db.ForeignKey('article_category.id'))
    # Hapus baris ini: user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Article {self.title}>'
