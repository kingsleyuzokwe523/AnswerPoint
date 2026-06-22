import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Try to import
try:
    from app import create_app
    print("Successfully imported app")
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Files in app folder: {os.listdir('app') if os.path.exists('app') else 'app folder not found'}")
    sys.exit(1)

app = create_app()

if __name__ == '__main__':
    print("Starting AnswerPoint server...")
    print("Visit http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
