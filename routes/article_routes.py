from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from models.article import Article, ArticleCategory
from extensions import db
from forms.article_forms import ArticleForm, ArticleCategoryForm
import os
from werkzeug.utils import secure_filename

article_bp = Blueprint('article', __name__)

@article_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    
    query = Article.query
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    articles = query.order_by(Article.created_at.desc()).paginate(page=page, per_page=9)
    categories = ArticleCategory.query.all()
    
    return render_template(
        'articles/index.html',
        articles=articles,
        categories=categories,
        current_category=category_id,
        title="Artikel Edukasi"
    )

@article_bp.route('/<int:id>')
def detail(id):
    article = Article.query.get_or_404(id)
    related_articles = Article.query.filter_by(category_id=article.category_id).filter(Article.id != id).limit(3).all()
    
    return render_template(
        'articles/detail.html',
        article=article,
        related_articles=related_articles,
        title=article.title
    )

@article_bp.route('/category/<int:id>')
def category(id):
    category = ArticleCategory.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    
    articles = Article.query.filter_by(category_id=id).order_by(Article.created_at.desc()).paginate(page=page, per_page=9)
    
    return render_template(
        'articles/category.html',
        category=category,
        articles=articles,
        title=f"Kategori: {category.name}"
    )