from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app import db
from app.models import Admin, Subject, Pin, Image, HomeContent, ExamTimetable
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime

admin_bp = Blueprint('admin', __name__)


# Admin login required decorator
def login_required(f):
    def wrapper(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):
            session['admin_logged_in'] = True
            session['admin_id'] = admin.id
            return redirect(url_for('admin.dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid credentials')

    return render_template('admin_login.html')


@admin_bp.route('/logout')
def logout():
    """Admin logout"""
    session.clear()
    return redirect(url_for('admin.login'))


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard"""
    total_pins = Pin.query.count()
    total_views = db.session.query(db.func.sum(Pin.views)).scalar() or 0
    total_subjects = Subject.query.count()
    total_images = Image.query.count()

    popular_pins = Pin.query.order_by(Pin.views.desc()).limit(5).all()
    recent_pins = Pin.query.order_by(Pin.created_at.desc()).limit(10).all()

    subjects_with_pins = db.session.query(
        Subject.name,
        Subject.exam_type,
        db.func.count(Pin.id).label('pin_count'),
        db.func.sum(Pin.views).label('total_views')
    ).outerjoin(Pin).group_by(Subject.id).order_by(db.func.count(Pin.id).desc()).all()

    all_subjects = Subject.query.order_by(Subject.name).all()
    timetable_entries = ExamTimetable.query.order_by(ExamTimetable.date).all()

    return render_template('admin_dashboard.html',
                           total_pins=total_pins,
                           total_views=total_views,
                           total_subjects=total_subjects,
                           total_images=total_images,
                           popular_pins=popular_pins,
                           recent_pins=recent_pins,
                           subjects_with_pins=subjects_with_pins,
                           all_subjects=all_subjects,
                           timetable_entries=timetable_entries)


@admin_bp.route('/create_pin', methods=['POST'])
@login_required
def create_pin():
    """Create a new PIN with text and images"""
    pin_code = request.form.get('pin_code', '').strip()
    subject_id = request.form.get('subject_id')
    answer_text = request.form.get('answer_text', '')

    # Validate PIN
    if not pin_code or len(pin_code) != 3 or not pin_code.isdigit():
        return jsonify({'success': False, 'error': 'PIN must be a 3-digit number (000-999)'})

    # Check if PIN exists
    existing = Pin.query.filter_by(pin_code=pin_code).first()
    if existing:
        return jsonify({'success': False, 'error': f'PIN {pin_code} already exists! Please use a different PIN.'})

    # Create PIN
    pin = Pin(pin_code=pin_code, subject_id=subject_id, answer_text=answer_text)
    db.session.add(pin)
    db.session.commit()

    # Handle image uploads
    if 'images' in request.files:
        files = request.files.getlist('images')
        for file in files:
            if file and file.filename:
                filename = secure_filename(f"{pin.id}_{datetime.now().timestamp()}_{file.filename}")
                filepath = os.path.join('uploads', filename)
                full_path = os.path.join('static', filepath)
                file.save(full_path)

                image = Image(pin_id=pin.id, image_path=filepath)
                db.session.add(image)

        db.session.commit()

    return jsonify({'success': True, 'message': f'PIN {pin_code} created successfully for {pin.subject.name}!'})


@admin_bp.route('/get_pin/<int:pin_id>', methods=['GET'])
@login_required
def get_pin(pin_id):
    """Get PIN details for editing"""
    pin = Pin.query.get_or_404(pin_id)
    return jsonify({
        'answer_text': pin.answer_text or '',
        'pin_code': pin.pin_code,
        'subject_id': pin.subject_id,
        'views': pin.views
    })


@admin_bp.route('/update_pin/<int:pin_id>', methods=['POST'])
@login_required
def update_pin(pin_id):
    """Update existing PIN answer text"""
    pin = Pin.query.get_or_404(pin_id)
    pin.answer_text = request.form.get('answer_text', '')
    db.session.commit()

    return jsonify({'success': True, 'message': 'PIN updated successfully'})


@admin_bp.route('/delete_pin/<int:pin_id>', methods=['POST'])
@login_required
def delete_pin(pin_id):
    """Delete a PIN and its images"""
    pin = Pin.query.get_or_404(pin_id)

    # Delete image files
    for image in pin.images:
        filepath = os.path.join('static', image.image_path)
        if os.path.exists(filepath):
            os.remove(filepath)

    db.session.delete(pin)
    db.session.commit()

    return jsonify({'success': True, 'message': 'PIN deleted successfully'})


@admin_bp.route('/bulk_create_pins', methods=['POST'])
@login_required
def bulk_create_pins():
    """Create multiple PINs at once for the same subject"""
    subject_id = request.form.get('subject_id')
    answer_text = request.form.get('answer_text', '')
    pin_range_start = int(request.form.get('pin_range_start'))
    pin_range_end = int(request.form.get('pin_range_end'))

    created = 0
    failed = []

    for pin_num in range(pin_range_start, pin_range_end + 1):
        pin_code = str(pin_num).zfill(3)
        existing = Pin.query.filter_by(pin_code=pin_code).first()

        if not existing:
            pin = Pin(pin_code=pin_code, subject_id=subject_id, answer_text=answer_text)
            db.session.add(pin)
            created += 1
        else:
            failed.append(pin_code)

    db.session.commit()

    subject = Subject.query.get(subject_id)
    return jsonify({
        'success': True,
        'created': created,
        'failed': failed,
        'message': f'Created {created} PINs for {subject.name}. Failed: {len(failed)}'
    })


@admin_bp.route('/update_content', methods=['POST'])
@login_required
def update_content():
    """Update home page content"""
    sections = ['hero_title', 'hero_text', 'announcement', 'instructions',
                'whatsapp_link', 'telegram_link', 'footer_text']

    for section in sections:
        content = request.form.get(section, '')
        home_content = HomeContent.query.filter_by(section=section).first()
        if home_content:
            home_content.content = content
        else:
            home_content = HomeContent(section=section, content=content)
            db.session.add(home_content)

    db.session.commit()
    return jsonify({'success': True, 'message': 'Home page content updated successfully!'})


@admin_bp.route('/get_home_content', methods=['GET'])
@login_required
def get_home_content():
    """Get current home page content for editing"""
    sections = ['hero_title', 'hero_text', 'announcement', 'instructions',
                'whatsapp_link', 'telegram_link', 'footer_text']

    content = {}
    for section in sections:
        home_content = HomeContent.query.filter_by(section=section).first()
        content[section] = home_content.content if home_content else ''

    return jsonify(content)


@admin_bp.route('/add_timetable', methods=['POST'])
@login_required
def add_timetable():
    """Add exam timetable entry - shows on home page"""
    exam_type = request.form.get('exam_type')
    subject = request.form.get('subject')
    paper = request.form.get('paper')
    date = request.form.get('date')
    time = request.form.get('time')
    year = request.form.get('year', 2026)

    entry = ExamTimetable(exam_type=exam_type, subject=subject, paper=paper,
                          date=date, time=time, year=year)
    db.session.add(entry)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Timetable entry added'})


@admin_bp.route('/delete_timetable/<int:entry_id>', methods=['POST'])
@login_required
def delete_timetable(entry_id):
    """Delete timetable entry"""
    entry = ExamTimetable.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Entry deleted'})


@admin_bp.route('/get_stats', methods=['GET'])
@login_required
def get_stats():
    """Get statistics for charts and dashboard"""
    stats = {
        'total_pins': Pin.query.count(),
        'total_views': db.session.query(db.func.sum(Pin.views)).scalar() or 0,
        'subjects_with_pins': db.session.query(Subject).join(Pin).distinct().count(),
        'total_images': Image.query.count(),
        'total_subjects': Subject.query.count(),
        'most_viewed_pin': None,
        'top_subjects': []
    }

    most_viewed = Pin.query.order_by(Pin.views.desc()).first()
    if most_viewed:
        stats['most_viewed_pin'] = {
            'pin': most_viewed.pin_code,
            'views': most_viewed.views,
            'subject': most_viewed.subject.name
        }

    # Top 5 subjects by views
    top_subjects = db.session.query(
        Subject.name,
        db.func.sum(Pin.views).label('total_views')
    ).join(Pin).group_by(Subject.id).order_by(db.func.sum(Pin.views).desc()).limit(5).all()

    stats['top_subjects'] = [{'name': s[0], 'views': s[1] or 0} for s in top_subjects]

    return jsonify(stats)