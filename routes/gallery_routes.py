from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
# from flask_login import login_required, current_user # Hapus impor ini
from models.gallery import GalleryImage, GalleryCategory
from extensions import db

gallery_bp = Blueprint('gallery', __name__)

@gallery_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)

    query = GalleryImage.query

    if category_id:
        query = query.filter_by(category_id=category_id)
    images = query.order_by(GalleryImage.created_at.desc()).paginate(page=page, per_page=12)
    categories = GalleryCategory.query.all()

    return render_template(
        'gallery/index.html',
        images=images,
        categories=categories,
        current_category=category_id,
        title="Galeri Masjid"
    )

@gallery_bp.route('/<int:id>')
def detail(id):
    image = GalleryImage.query.get_or_404(id)

    # Get next and previous images in the same category
    next_image = GalleryImage.query.filter(
        GalleryImage.category_id == image.category_id,
        GalleryImage.id > image.id
    ).order_by(GalleryImage.id).first()

    prev_image = GalleryImage.query.filter(
        GalleryImage.category_id == image.category_id,
        GalleryImage.id < image.id
    ).order_by(GalleryImage.id.desc()).first()

    return render_template(
        'gallery/detail.html',
        image=image,
        next_image=next_image,
        prev_image=prev_image,
        title=image.title
    )
