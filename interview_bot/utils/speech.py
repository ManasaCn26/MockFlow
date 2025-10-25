import pyttsx3
from flask import session, render_template
from config import QUESTION_BANKS

def speak_question():
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
        engine = pyttsx3.init()
        engine.say(current_question)
        engine.runAndWait()
    except Exception as e:
        print(f"Text-to-speech error: {e}")
    
    return render_template('base.html', QUESTION_BANKS=QUESTION_BANKS)