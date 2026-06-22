import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Try to import from the NEW application.py file
try:
    from app.application import create_app  # ✅ Changed from 'app' to 'app.application'
    print("✅ Successfully imported app from application.py")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"📁 Current directory: {os.getcwd()}")
    if os.path.exists('app'):
        print(f"📂 Files in app folder: {os.listdir('app')}")
    else:
        print("❌ app folder not found!")
    sys.exit(1)

app = create_app()

if __name__ == '__main__':
    print("🚀 Starting AnswerPoint server...")
    print("🌐 Visit http://localhost:5000")
    print("Press CTRL+C to stop")
    app.run(debug=True, host='0.0.0.0', port=5000)
