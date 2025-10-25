import random

def analyze_answer(answer, question):
    """🎯 Analyze user's answer with proper scoring"""
    word_count = len(answer.split())
    
    # Quality score (1-10) - More realistic scoring
    quality_score = 5  # Base score
    
    # Word count scoring
    if word_count >= 30 and word_count < 50:
        quality_score += 0.5
    elif word_count >= 50 and word_count < 100:
        quality_score += 1
    elif word_count >= 100 and word_count < 200:
        quality_score += 1.5
    elif word_count >= 200:
        quality_score += 2
    
    # Content quality indicators
    if 'i ' in answer.lower() or 'my ' in answer.lower() or 'me ' in answer.lower():
        quality_score += 1  # Personal examples
    
    if any(word in answer.lower() for word in ['because', 'therefore', 'so', 'thus']):
        quality_score += 1  # Logical reasoning
    
    if any(word in answer.lower() for word in ['learned', 'improved', 'grew', 'developed']):
        quality_score += 1  # Growth mindset
    
    if any(word in answer.lower() for word in ['team', 'collaborat', 'work with']):
        quality_score += 0.5  # Teamwork
    
    if any(word in answer.lower() for word in ['result', 'impact', 'achieved', 'success']):
        quality_score += 0.5  # Results-oriented
    
    # Ensure score is between 1-10
    quality_score = max(1, min(10, round(quality_score, 1)))
    
    # Generate feedback
    feedback_parts = []
    
    # Word count feedback
    if word_count < 30:
        feedback_parts.append("❌ Too short. Aim for 50-150 words with specific examples.")
    elif word_count < 50:
        feedback_parts.append("⚠️ Good start, but add more details and examples.")
    elif word_count < 100:
        feedback_parts.append("✅ Good length with adequate detail.")
    elif word_count < 200:
        feedback_parts.append("✅ Excellent! Detailed and comprehensive answer.")
    else:
        feedback_parts.append("⚠️ Very detailed! Consider being more concise.")
    
    # Content feedback
    if 'i ' not in answer.lower():
        feedback_parts.append("💡 Add more personal examples using 'I' statements.")
    
    if not any(word in answer.lower() for word in ['because', 'therefore']):
        feedback_parts.append("💡 Explain your reasoning with 'because' or 'therefore'.")
    
    # Motivational feedback
    motivational = [
        "🚀 Great thinking! Your approach shows good problem-solving skills.",
        "💡 Well structured! You're communicating your ideas clearly.",
        "⚡ Good energy! Your confidence comes through in your writing.",
        "🎯 On target! You're addressing the key points effectively.",
        "🌟 Impressive! You're demonstrating strong communication skills."
    ]
    feedback_parts.append(random.choice(motivational))
    
    return {
        'word_count': word_count,
        'quality_score': quality_score,
        'feedback': " ".join(feedback_parts)
    }