from flask import Blueprint, session, redirect, render_template
from models import get_user_scores, save_user_score
from config import QUESTION_BANKS

score_bp = Blueprint('score', __name__)

@score_bp.route('/scores')
def scores():
    """Display user scores"""
    if not session.get('username'):
        return redirect('/')
    
    try:
        username = session['username']
        user_scores = get_user_scores(username)
        
        # Create scores HTML
        scores_html = f'''
        <div class="card">
            <h2>📊 Your Interview Scores</h2>
            <p><strong>Username:</strong> {username}</p>
        '''
        
        if user_scores:
            for score_id, score_data in user_scores.items():
                scores_html += f'''
                <div class="card" style="background: #f8f9fa; margin: 10px 0;">
                    <h3>🎯 {score_data['field'].title()} Interview</h3>
                    <p><strong>Date:</strong> {score_data['date']}</p>
                    <p><strong>Final Score:</strong> {score_data['total_score']:.1f}/10</p>
                    <p><strong>Question Scores:</strong> {', '.join(map(str, score_data['scores']))}</p>
                </div>
                '''
        else:
            scores_html += '<p>No scores yet. Complete an interview to see your scores here!</p>'
        
        scores_html += '<br><a href="/" class="btn">🏠 Back to Home</a></div>'
        
        # Return complete HTML page
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>🚀 AI Interview Coach - Scores</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 20px; }}
                .card {{ background: white; padding: 20px; border-radius: 10px; margin: 10px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .btn {{ background: #667eea; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; margin: 5px; text-decoration: none; display: inline-block; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 AI Interview Coach</h1>
                <p>Your Performance History</p>
                <div style="background: #e8f5e8; padding: 10px; border-radius: 5px; margin: 10px 0;">
                    👤 Welcome, <strong>{username}</strong>! 
                    | <a href="/" style="color: white;">🏠 Home</a>
                    | <a href="/logout" style="color: white;">🚪 Logout</a>
                </div>
            </div>
            {scores_html}
        </body>
        </html>
        '''
        
    except Exception as e:
        return f"Error loading scores: {str(e)}"

@score_bp.route('/save_score', methods=['POST'])
def save_score():
    """Save current interview score"""
    try:
        if not session.get('username') or not session.get('answers'):
            return redirect('/')
        
        # Extract scores from answers
        scores = [answer['analysis']['quality_score'] for answer in session['answers']]
        field = session['field']
        username = session['username']
        
        # Save to database
        if save_user_score(username, field, scores):
            print(f"✅ Score saved successfully for {username}")
            # Clear interview progress after saving score
            from models import clear_interview_progress
            clear_interview_progress(username)
            
            # Clear interview session but keep username
            session.pop('field', None)
            session.pop('round', None)
            session.pop('question_num', None)
            session.pop('answers', None)
            session.pop('show_congrats', None)
        else:
            print("❌ Failed to save score")
        
        return redirect('/')
        
    except Exception as e:
        print(f"❌ Error in save_score: {e}")
        return redirect('/')