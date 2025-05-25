from flask import Blueprint, render_template, request, current_app
from models.mosque import MosqueInfo, QuoteOfTheDay
from models.lecture import Lecture
from models.article import Article
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Get mosque info
    mosque_info = MosqueInfo.query.first()
    
    # Get active quote of the day
    quote = QuoteOfTheDay.query.filter_by(is_active=True).first()
    
    # Get upcoming lectures (next 7 days)
    today = datetime.now()
    next_week = today + timedelta(days=7)
    upcoming_lectures = Lecture.query.filter(
        Lecture.date >= today,
        Lecture.date <= next_week
    ).order_by(Lecture.date).limit(5).all()
    
    # Get latest articles
    latest_articles = Article.query.order_by(Article.created_at.desc()).limit(3).all()
    
    return render_template(
        'index.html',
        mosque_info=mosque_info,
        quote=quote,
        upcoming_lectures=upcoming_lectures,
        latest_articles=latest_articles,
        title="Beranda",
        now=datetime.now()  # ✅ Kirim now ke template
    )

@main_bp.route('/about')
def about():
    mosque_info = MosqueInfo.query.first()
    return render_template(
        'about.html',
        mosque_info=mosque_info,
        title="Tentang Kami",
        now=datetime.now()  # ✅ Kirim now juga ke halaman ini jika pakai {{ now.year }} di base.html
    )

@main_bp.route('/contact')
def contact():
    mosque_info = MosqueInfo.query.first()
    return render_template(
        'contact.html',
        mosque_info=mosque_info,
        title="Kontak",
        now=datetime.now()  # ✅ Sama seperti atas
    )
