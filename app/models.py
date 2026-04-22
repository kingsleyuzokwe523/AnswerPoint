from app import db
from datetime import datetime

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    exam_type = db.Column(db.String(10), nullable=False)
    has_practical = db.Column(db.Boolean, default=False)
    display_order = db.Column(db.Integer, default=0)
    pins = db.relationship('Pin', backref='subject', lazy=True)

class Pin(db.Model):
    __tablename__ = 'pins'
    id = db.Column(db.Integer, primary_key=True)
    pin_code = db.Column(db.String(3), nullable=False, unique=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    answer_text = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    images = db.relationship('Image', backref='pin', lazy=True, cascade='all, delete-orphan')

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    pin_id = db.Column(db.Integer, db.ForeignKey('pins.id'), nullable=False)
    image_path = db.Column(db.String(500), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class HomeContent(db.Model):
    __tablename__ = 'home_content'
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(50), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=True)

class ExamTimetable(db.Model):
    __tablename__ = 'exam_timetables'
    id = db.Column(db.Integer, primary_key=True)
    exam_type = db.Column(db.String(10), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    paper = db.Column(db.String(100), nullable=True)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, default=2026)