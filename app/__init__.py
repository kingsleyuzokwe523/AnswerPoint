# app/__init__.py
"""
AnswerPoint Application - Main package
Re-exports from application.py
"""
from app.application import create_app, db

__all__ = ['create_app', 'db']
