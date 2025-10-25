from flask import Flask, render_template, session
import os
import json
from routes.auth_routes import auth_bp
from routes.interview_routes import interview_bp
from routes.score_routes import score_bp
from config import QUESTION_BANKS
from utils.browser import open_browser
import threading

app = Flask(__name__)
app.secret_key = 'interview_bot_secret_key_123'

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(interview_bp)
app.register_blueprint(score_bp)

@app.route('/')
def home():
    from models import load_interview_progress
    
    progress_data = {}
    if session.get('username'):
        progress_data = load_interview_progress(session['username'])
    
    return render_template('base.html', 
                         QUESTION_BANKS=QUESTION_BANKS,
                         progress_data=progress_data)

@app.route('/debug')
def debug():
    """Debug page to check database status"""
    from models import load_users
    users = load_users()
    
    debug_info = f"""
    <h2>🔧 Debug Information</h2>
    <p><strong>Database File:</strong> users.json</p>
    <p><strong>Database Exists:</strong> {os.path.exists('users.json')}</p>
    <p><strong>Total Users:</strong> {len(users)}</p>
    <p><strong>Current Session:</strong> {dict(session)}</p>
    <h3>Users in Database:</h3>
    <pre>{json.dumps(users, indent=2)}</pre>
    """
    return debug_info

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 STARTING AI INTERVIEW COACH")
    print("=" * 60)
    print("📡 Starting server on http://localhost:5000")
    print("⏳ Please wait 3 seconds...")
    print("🌐 Browser will open automatically!")
    print("=" * 60)
    
    try:
        # Start browser in background thread
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Start Flask app WITH DEBUG MODE to see errors
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")