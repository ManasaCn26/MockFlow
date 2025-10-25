from flask import Blueprint, request, session, redirect, render_template
from models import load_users, save_users, load_interview_progress
from config import QUESTION_BANKS

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    users = load_users()
    
    if username in users and users[username]['password'] == password:
        session['username'] = username
        print(f"✅ User logged in: {username}")
        
        # Load progress data for this user
        progress_data = load_interview_progress(username)
        return render_template('base.html', 
                             QUESTION_BANKS=QUESTION_BANKS,
                             progress_data=progress_data)
    else:
        return "❌ Invalid credentials. <a href='/'>Go back</a>"

@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    
    users = load_users()
    
    if username in users:
        return "❌ Username already exists. <a href='/'>Go back</a>"
    
    # Create new user
    users[username] = {
        'password': password, 
        'scores': {},
        'current_interview': {}
    }
    
    if save_users(users):
        session['username'] = username
        print(f"✅ New user registered: {username}")
        
        # New user has no progress data
        progress_data = {}
        return render_template('base.html', 
                             QUESTION_BANKS=QUESTION_BANKS,
                             progress_data=progress_data)
    else:
        return "❌ Registration failed. <a href='/'>Go back</a>"

@auth_bp.route('/logout')
def logout():
    username = session.get('username', 'Unknown')
    session.clear()
    print(f"✅ User logged out: {username}")
    return redirect('/')