from flask import Blueprint, render_template, jsonify

# Create blueprint
main_bp = Blueprint('main', __name__)

# Simple home route
@main_bp.route('/')
def index():
    return "AnswerPoint is working! 🎉"

# Simple test route
@main_bp.route('/test')
def test():
    return jsonify({'status': 'success', 'message': 'Routes are working!'})

# Your get_answer route - minimal version
@main_bp.route('/get_answer', methods=['POST'])
def get_answer():
    from flask import request
    pin_code = request.form.get('pin_code', '')
    return jsonify({
        'success': True,
        'answer_text': f'<p>Answer for PIN: {pin_code}</p>',
        'subject_name': 'Test Subject',
        'pin_code': pin_code
    })
