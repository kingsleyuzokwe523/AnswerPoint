import os
from werkzeug.utils import secure_filename
from flask import current_app
from PIL import Image as PILImage


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_image(file, pin_id):
    """Save uploaded image and return path"""
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{pin_id}_{file.filename}")
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        # Optimize image
        img = PILImage.open(file)
        img.thumbnail((800, 800))
        img.save(filepath, optimize=True, quality=85)

        return os.path.join('uploads', filename)
    return None


def format_date(date_obj):
    """Format date for display"""
    if date_obj:
        return date_obj.strftime('%b %d, %Y at %I:%M %p')
    return 'N/A'