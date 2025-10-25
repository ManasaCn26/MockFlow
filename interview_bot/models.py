import json
import os
from datetime import datetime

USER_DB_FILE = 'users.json'

def load_users():
    """Load users from JSON file"""
    try:
        if os.path.exists(USER_DB_FILE):
            with open(USER_DB_FILE, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading users: {e}")
        return {}

def save_users(users):
    """Save users to JSON file"""
    try:
        with open(USER_DB_FILE, 'w') as f:
            json.dump(users, f, indent=2)
        print(f"✅ Users saved successfully! Total users: {len(users)}")
        return True
    except Exception as e:
        print(f"❌ Error saving users: {e}")
        return False

def save_interview_progress(username, interview_data):
    """Save current interview progress"""
    try:
        users = load_users()
        
        if username not in users:
            users[username] = {'password': '', 'scores': {}, 'current_interview': {}}
        
        users[username]['current_interview'] = interview_data
        
        if save_users(users):
            print(f"✅ Interview progress saved for {username}")
            return True
        return False
        
    except Exception as e:
        print(f"❌ Error saving progress: {e}")
        return False

def load_interview_progress(username):
    """Load current interview progress"""
    try:
        users = load_users()
        return users.get(username, {}).get('current_interview', {})
    except Exception as e:
        print(f"❌ Error loading progress: {e}")
        return {}

def clear_interview_progress(username):
    """Clear current interview progress"""
    try:
        users = load_users()
        if username in users and 'current_interview' in users[username]:
            users[username]['current_interview'] = {}
            return save_users(users)
        return True
    except Exception as e:
        print(f"❌ Error clearing progress: {e}")
        return False

def save_user_score(username, field, scores):
    """Save user score to database"""
    try:
        users = load_users()
        
        # Create user if doesn't exist
        if username not in users:
            users[username] = {'password': '', 'scores': {}, 'current_interview': {}}
        
        # Ensure scores key exists
        if 'scores' not in users[username]:
            users[username]['scores'] = {}
        
        # Create unique score ID
        score_id = f"{field}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Save score data
        users[username]['scores'][score_id] = {
            'field': field,
            'scores': scores,
            'total_score': sum(scores) / len(scores) if scores else 0,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save to file
        if save_users(users):
            print(f"✅ Score saved for {username}: {score_id}")
            return True
        return False
        
    except Exception as e:
        print(f"❌ Error saving score: {e}")
        return False

def get_user_scores(username):
    """Get all scores for a user"""
    try:
        users = load_users()
        return users.get(username, {}).get('scores', {})
    except Exception as e:
        print(f"❌ Error getting scores: {e}")
        return {}