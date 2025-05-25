from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from models.lecture import Lecture, LectureCategory
from models.article import Article, ArticleCategory
from models.gallery import GalleryImage, GalleryCategory
from models.mosque import MosqueInfo, QuoteOfTheDay
from models.user import User
from extensions import db
from forms.lecture_forms import LectureForm, LectureCategoryForm
from forms.article_forms import ArticleForm, ArticleCategoryForm
from forms.gallery_forms import GalleryImageForm, GalleryCategoryForm
from forms.mosque_forms import MosqueInfoForm, QuoteForm
from datetime import datetime
import os
from werkzeug.utils import secure_filename

admin_bp = Blueprint('admin', __name__)

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need admin privileges to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def index():
    # Dashboard overview
    total_lectures = Lecture.query.count()
    total_articles = Article.query.count()
    total_gallery = GalleryImage.query.count()
    total_users = User.query.count()
    
    # Recent content
    recent_lectures = Lecture.query.order_by(Lecture.created_at.desc()).limit(5).all()
    recent_articles = Article.query.order_by(Article.created_at.desc()).limit(5).all()
    
    # Upcoming lectures
    upcoming_lectures = Lecture.query.filter(
        Lecture.date >= datetime.utcnow()
    ).order_by(Lecture.date).limit(5).all()
    
    return render_template(
        'admin/index.html',
        total_lectures=total_lectures,
        total_articles=total_articles,
        total_gallery=total_gallery,
        total_users=total_users,
        recent_lectures=recent_lectures,
        recent_articles=recent_articles,
        upcoming_lectures=upcoming_lectures,
        title="Admin Dashboard"
    )

# Lecture management
@admin_bp.route('/lectures')
@login_required
@admin_required
def lectures():
    lectures = Lecture.query.order_by(Lecture.date.desc()).all()
    return render_template('admin/lectures/index.html', lectures=lectures, title="Manage Lectures")

@admin_bp.route('/lectures/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_lecture():
    form = LectureForm()
    form.category_id.choices = [(c.id, c.name) for c in LectureCategory.query.all()]
    
    if form.validate_on_submit():
        lecture = Lecture(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            duration=form.duration.data,
            location=form.location.data,
            speaker=form.speaker.data,
            youtube_link=form.youtube_link.data,
            category_id=form.category_id.data,
            user_id=current_user.id
        )
        
        # Handle file upload
        if form.materials_file.data:
            filename = secure_filename(form.materials_file.data.filename)
            form.materials_file.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'lectures', filename))
            lecture.materials_file = filename
            
        if form.image.data:
            image_filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'lectures', image_filename))
            lecture.image = image_filename
            
        db.session.add(lecture)
        db.session.commit()
        flash('Lecture created successfully!', 'success')
        return redirect(url_for('admin.lectures'))
        
    return render_template('admin/lectures/create.html', form=form, title="Create Lecture")

# Article management
@admin_bp.route('/articles')
@login_required
@admin_required
def articles():
    articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template('admin/articles/index.html', articles=articles, title="Manage Articles")

# Gallery management
@admin_bp.route('/gallery')
@login_required
@admin_required
def gallery():
    images = GalleryImage.query.order_by(GalleryImage.created_at.desc()).all()
    return render_template('admin/gallery/index.html', images=images, title="Manage Gallery")

# Mosque info management
@admin_bp.route('/mosque-info', methods=['GET', 'POST'])
@login_required
@admin_required
def mosque_info():
    mosque = MosqueInfo.query.first()
    if not mosque:
        mosque = MosqueInfo(name='Masjid Default', address='Alamat Default')
        db.session.add(mosque)
        db.session.commit()
        
    form = MosqueInfoForm(obj=mosque)
    
    if form.validate_on_submit():
        form.populate_obj(mosque)
        
        # Handle logo upload
        if form.logo.data:
            logo_filename = secure_filename(form.logo.data.filename)
            form.logo.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], logo_filename))
            mosque.logo = logo_filename
            
        # Handle QRIS image upload
        if form.qris_image.data:
            qris_filename = secure_filename(form.qris_image.data.filename)
            form.qris_image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], qris_filename))
            mosque.qris_image = qris_filename
            
        db.session.commit()
        flash('Mosque information updated successfully!', 'success')
        return redirect(url_for('admin.mosque_info'))
        
    return render_template('admin/mosque/info.html', form=form, mosque=mosque, title="Mosque Information")

# Quote management
@admin_bp.route('/quotes')
@login_required
@admin_required
def quotes():
    quotes = QuoteOfTheDay.query.all()
    return render_template('admin/mosque/quotes.html', quotes=quotes, title="Manage Quotes")