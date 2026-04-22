from flask import Blueprint, render_template, request, jsonify, session
from app import db
from app.models import Subject, Pin, Image, HomeContent, ExamTimetable
import os

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Home page"""
    # Get home content
    hero_title = HomeContent.query.filter_by(section='hero_title').first()
    hero_text = HomeContent.query.filter_by(section='hero_text').first()
    announcement = HomeContent.query.filter_by(section='announcement').first()
    instructions = HomeContent.query.filter_by(section='instructions').first()
    whatsapp_link = HomeContent.query.filter_by(section='whatsapp_link').first()
    telegram_link = HomeContent.query.filter_by(section='telegram_link').first()
    footer_text = HomeContent.query.filter_by(section='footer_text').first()

    # Get all subjects grouped by exam type
    waec_subjects = Subject.query.filter_by(exam_type='WAEC').order_by(Subject.name).all()
    neco_subjects = Subject.query.filter_by(exam_type='NECO').order_by(Subject.name).all()

    # Get exam timetables
    waec_timetable = ExamTimetable.query.filter_by(exam_type='WAEC', year=2026).order_by(ExamTimetable.date).all()
    neco_timetable = ExamTimetable.query.filter_by(exam_type='NECO', year=2026).order_by(ExamTimetable.date).all()

    return render_template('index.html',
                           hero_title=hero_title.content if hero_title else "AnswerPoint",
                           hero_text=hero_text.content if hero_text else "",
                           announcement=announcement.content if announcement else "",
                           instructions=instructions.content if instructions else "",
                           whatsapp_link=whatsapp_link.content if whatsapp_link else "#",
                           telegram_link=telegram_link.content if telegram_link else "#",
                           footer_text=footer_text.content if footer_text else "",
                           waec_subjects=waec_subjects,
                           neco_subjects=neco_subjects,
                           waec_timetable=waec_timetable,
                           neco_timetable=neco_timetable)


@main_bp.route('/get_answer', methods=['POST'])
def get_answer():
    """Get answer for a PIN"""
    pin_code = request.form.get('pin_code', '').strip()

    if not pin_code or len(pin_code) != 3 or not pin_code.isdigit():
        return jsonify({'success': False, 'error': 'Invalid PIN. Please enter a 3-digit number.'})

    # Find the PIN
    pin = Pin.query.filter_by(pin_code=pin_code).first()

    if not pin:
        return jsonify({'success': False, 'error': 'PIN not found. Please check and try again.'})

    # Increment view count
    pin.views += 1
    db.session.commit()

    # Get subject details
    subject = pin.subject

    # Get images
    images = []
    for img in pin.images:
        images.append(img.image_path.replace('\\', '/'))

    return jsonify({
        'success': True,
        'subject': subject.name,
        'exam_type': subject.exam_type,
        'answer_text': pin.answer_text or '',
        'images': images,
        'views': pin.views
    })


@main_bp.route('/subjects')
def subjects():
    """View all subjects"""
    exam_type = request.args.get('exam', 'all')
    search = request.args.get('search', '')

    query = Subject.query
    if exam_type != 'all':
        query = query.filter_by(exam_type=exam_type)
    if search:
        query = query.filter(Subject.name.contains(search))

    subjects_list = query.order_by(Subject.name).all()

    return render_template('subjects.html', subjects=subjects_list, exam_type=exam_type, search=search)