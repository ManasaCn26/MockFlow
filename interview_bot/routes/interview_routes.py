from flask import Blueprint, request, session, render_template, redirect
from config import QUESTION_BANKS
from utils.analysis import analyze_answer
from utils.speech import speak_question
from models import save_interview_progress, load_interview_progress, clear_interview_progress

interview_bp = Blueprint('interview', __name__)

def get_progress_data():
    """Helper function to get progress data for current user"""
    if session.get('username'):
        return load_interview_progress(session['username'])
    return {}

@interview_bp.route('/start', methods=['POST'])
def start_interview():
    if not session.get('username'):
        return redirect('/')
    
    session['field'] = request.form['field']
    session['round'] = 1
    session['question_num'] = 0
    session['answers'] = []
    
    # Save progress to database
    save_interview_progress(session['username'], {
        'field': session['field'],
        'round': session['round'],
        'question_num': session['question_num'],
        'answers': session['answers']
    })
    
    return render_template('base.html', 
                         QUESTION_BANKS=QUESTION_BANKS,
                         progress_data=get_progress_data())

@interview_bp.route('/resume_interview')
def resume_interview():
    """Resume unfinished interview"""
    if not session.get('username'):
        return redirect('/')
    
    # Load progress from database
    progress = load_interview_progress(session['username'])
    
    if progress and progress.get('field'):
        session['field'] = progress['field']
        session['round'] = progress['round']
        session['question_num'] = progress['question_num']
        session['answers'] = progress['answers']
        print(f"✅ Resumed interview: {session['field']} - Round {session['round']} - Q{session['question_num'] + 1}")
    else:
        # No progress to resume
        return redirect('/')
    
    return render_template('base.html', 
                         QUESTION_BANKS=QUESTION_BANKS,
                         progress_data=get_progress_data())

@interview_bp.route('/answer', methods=['POST'])
def submit_answer():
    if not session.get('username') or not session.get('field'):
        return redirect('/')
    
    field = session['field']
    round_num = session['round']
    question_num = session['question_num']
    
    round_names = list(QUESTION_BANKS[field].keys())
    current_round_name = round_names[round_num - 1]
    questions = QUESTION_BANKS[field][current_round_name]
    
    current_q = questions[question_num]
    answer = request.form['answer']
    
    # Analyze answer with proper scoring
    analysis = analyze_answer(answer, current_q)
    
    # Add to answers
    session['answers'].append({
        'question': current_q,
        'answer': answer,
        'analysis': analysis
    })
    
    # Move to next question
    session['question_num'] += 1
    
    # Save progress after each answer
    save_interview_progress(session['username'], {
        'field': session['field'],
        'round': session['round'],
        'question_num': session['question_num'],
        'answers': session['answers']
    })
    
    # Check if round is completed to show congrats
    if session['question_num'] >= len(questions):
        session['show_congrats'] = True
    
    return render_template('base.html', 
                         QUESTION_BANKS=QUESTION_BANKS,
                         progress_data=get_progress_data())

@interview_bp.route('/next_round', methods=['POST'])
def next_round():
    session['round'] += 1
    session['question_num'] = 0
    session['show_congrats'] = True
    
    # Save progress
    save_interview_progress(session['username'], {
        'field': session['field'],
        'round': session['round'],
        'question_num': session['question_num'],
        'answers': session['answers']
    })
    
    return render_template('base.html', 
                         QUESTION_BANKS=QUESTION_BANKS,
                         progress_data=get_progress_data())

@interview_bp.route('/speak', methods=['POST'])
def speak():
    if not session.get('username') or not session.get('field'):
        return redirect('/')
    
    # Get current question
    field = session['field']
    round_num = session['round']
    question_num = session['question_num']
    
    round_names = list(QUESTION_BANKS[field].keys())
    current_round_name = round_names[round_num - 1]
    questions = QUESTION_BANKS[field][current_round_name]
    current_question = questions[question_num]
    
    # Speak the question
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(current_question)
        engine.runAndWait()
    except Exception as e:
        print(f"Text-to-speech error: {e}")
    
    return render_template('base.html', 
                         QUESTION_BANKS=QUESTION_BANKS,
                         progress_data=get_progress_data())

@interview_bp.route('/restart', methods=['POST'])
def restart():
    """Start a new interview (clear current progress)"""
    if session.get('username'):
        clear_interview_progress(session['username'])
    
    session.pop('field', None)
    session.pop('round', None)
    session.pop('question_num', None)
    session.pop('answers', None)
    session.pop('show_congrats', None)
    
    return render_template('base.html', 
                         QUESTION_BANKS=QUESTION_BANKS,
                         progress_data=get_progress_data())

@interview_bp.route('/close_modal')
def close_modal():
    """Remove the show_congrats flag from session"""
    session.pop('show_congrats', None)
    return render_template('base.html', 
                         QUESTION_BANKS=QUESTION_BANKS,
                         progress_data=get_progress_data())

@interview_bp.route('/submit_voice', methods=['POST'])
def submit_voice_answer():
    """Handle voice answer submission"""
    if not session.get('username') or not session.get('field'):
        return redirect('/')
    
    try:
        # Get audio data from form
        audio_data = request.form.get('audio_data')
        
        if not audio_data:
            return "No audio data received", 400
        
        # For now, we'll just save the audio data to session
        # In a real app, you would:
        # 1. Save audio file to disk or cloud storage
        # 2. Transcribe using speech-to-text API
        # 3. Analyze the transcribed text
        
        field = session['field']
        round_num = session['round']
        question_num = session['question_num']
        
        round_names = list(QUESTION_BANKS[field].keys())
        current_round_name = round_names[round_num - 1]
        questions = QUESTION_BANKS[field][current_round_name]
        current_q = questions[question_num]
        
        # Create a placeholder analysis for voice answers
        analysis = {
            'word_count': 0,  # Would be from transcription
            'quality_score': 6,  # Base score for voice answers
            'feedback': "🎤 Voice answer recorded! (Transcription not implemented yet)"
        }
        
        # Add to answers
        session['answers'].append({
            'question': current_q,
            'answer': '[Voice Recording]',  # Placeholder
            'analysis': analysis,
            'audio_data': audio_data  # Store base64 audio data
        })
        
        # Move to next question
        session['question_num'] += 1
        
        # Save progress
        save_interview_progress(session['username'], {
            'field': session['field'],
            'round': session['round'],
            'question_num': session['question_num'],
            'answers': session['answers']
        })
        
        # Check if round is completed
        if session['question_num'] >= len(questions):
            session['show_congrats'] = True
        
        return render_template('base.html', 
                             QUESTION_BANKS=QUESTION_BANKS,
                             progress_data=get_progress_data())
        
    except Exception as e:
        print(f"❌ Error processing voice answer: {e}")
        return redirect('/')