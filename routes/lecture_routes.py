from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
# from flask_login import login_required, current_user # Hapus impor ini
from models.lecture import Lecture, LectureCategory
from extensions import db
from forms.lecture_forms import LectureForm, LectureCategoryForm
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from sqlalchemy import extract, text

lecture_bp = Blueprint('lecture', __name__)

@lecture_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)

    # Build base query
    query = Lecture.query

    # Apply filters
    if category_id:
        query = query.filter_by(category_id=category_id)
    if month:
        query = query.filter(extract('month', Lecture.date) == month)
    if year:
        query = query.filter(extract('year', Lecture.date) == year)

    # Get current time
    now = datetime.utcnow()

    # METHOD 1: Simple sorting (recommended for most cases)
    lectures = query.order_by(
        # Priority: upcoming lectures first (False=0), past lectures second (True=1)
          (Lecture.date < now),
        # Then sort all by date descending (most recent/nearest first)
        Lecture.date.desc()
    ).paginate(page=page, per_page=10)

    # METHOD 2: If you need precise control (upcoming asc, past desc)
    # Uncomment this section and comment METHOD 1 above
    """
    # Split queries for precise control
    upcoming_query = query.filter(Lecture.date >= now)
    past_query = query.filter(Lecture.date < now)

    # Calculate pagination
    per_page = 10
    offset = (page - 1) * per_page

    # Get upcoming lectures count
    upcoming_count = upcoming_query.count()

    if offset < upcoming_count:
        # We're still in upcoming lectures
        upcoming_lectures = upcoming_query.order_by(Lecture.date.asc()).limit(per_page).offset(offset).all()
        remaining_slots = per_page - len(upcoming_lectures)

        if remaining_slots > 0:
            # Fill remaining slots with past lectures
            past_lectures = past_query.order_by(Lecture.date.desc()).limit(remaining_slots).all()
            all_lectures = upcoming_lectures + past_lectures
        else:
            all_lectures = upcoming_lectures
    else:
        # We're in past lectures section
        past_offset = offset - upcoming_count
        all_lectures = past_query.order_by(Lecture.date.desc()).limit(per_page).offset(past_offset).all()
    # Get total count
    total_count = query.count()

    # Create pagination object
    class CustomPagination:
        def __init__(self, items, page, per_page, total):
            self.items = items
            self.page = page
            self.per_page = per_page
            self.total = total
            self.pages = (total + per_page - 1) // per_page if total > 0 else 1
            self.has_prev = page > 1
            self.has_next = page < self.pages
            self.prev_num = page - 1 if self.has_prev else None
            self.next_num = page + 1 if self.has_next else None
        lectures = CustomPagination(all_lectures, page, per_page, total_count)
    """
    categories = LectureCategory.query.all()

    # Get available years and months for filtering
    years = db.session.query(extract('year', Lecture.date).distinct()).all()
    years = [int(y[0]) for y in years if y[0]]

    return render_template(
        'lectures/index.html',
        lectures=lectures,
        categories=categories,
        current_category=category_id,
        current_month=month,
        current_year=year,
        years=years,
        title="Jadwal Kajian"
    )

@lecture_bp.route('/calendar')
def calendar():
    # Get all lectures for calendar view
    lectures = Lecture.query.all()
    categories = LectureCategory.query.all()

    # Convert to calendar-friendly format
    events = []
    for lecture in lectures:
        events.append({
            'id': lecture.id,
            'title': lecture.title,
            'start': lecture.date.isoformat(),
            'end': (lecture.date + timedelta(minutes=lecture.duration or 60)).isoformat() if lecture.duration else None,
            'url': url_for('lecture.detail', id=lecture.id),
            'classNames': [f'category-{lecture.category_id}'],
            'description': lecture.description
        })
    return render_template(
        'lectures/calendar.html',
        events=events,
        categories=categories,
        title="Kalender Kajian"
    )

@lecture_bp.route('/<int:id>')
def detail(id):
    lecture = Lecture.query.get_or_404(id)
    related_lectures = Lecture.query.filter_by(category_id=lecture.category_id).filter(Lecture.id != id).limit(3).all()

    return render_template(
        'lectures/detail.html',
        lecture=lecture,
        related_lectures=related_lectures,
        title=lecture.title
    )

@lecture_bp.route('/archive')
def archive():
    page = request.args.get('page', 1, type=int)

    # Get only past lectures with videos
    now = datetime.utcnow()
    lectures = Lecture.query.filter(
        Lecture.date < now,
        Lecture.youtube_link.isnot(None)
    ).order_by(Lecture.date.desc()).paginate(page=page, per_page=12)

    return render_template(
        'lectures/archive.html',
        lectures=lectures,
        title="Arsip Kajian"
    )

@lecture_bp.route('/add', methods=['GET', 'POST'])
# @login_required # Hapus dekorator ini
def add():
    # if not current_user.is_admin: # Hapus atau ubah logika ini
    #     flash('Hanya admin yang dapat menambah kajian.', 'danger')
    #     return redirect(url_for('lecture.index'))
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
            category_id=form.category_id.data
        )
        # Handle file uploads if needed (image, materials_file)
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(current_app.root_path, 'static/uploads/lectures', filename))
            lecture.image = filename
        if form.materials_file.data:
            filename = secure_filename(form.materials_file.data.filename)
            form.materials_file.data.save(os.path.join(current_app.root_path, 'static/uploads/lectures', filename))
            lecture.materials_file = filename
        db.session.add(lecture)
        db.session.commit()
        flash('Kajian berhasil ditambahkan.', 'success')
        return redirect(url_for('lecture.index'))
    return render_template('lectures/add.html', form=form)
