# moods.py

def detect_mood(user_input):
    user_input = user_input.lower()

    if any(word in user_input for word in ['sad', 'mood off', 'depressed']):
        return "sad"
    
    elif any(word in user_input for word in ['good mood', 'happy', 'excited']):
        return "happy"
    
    elif any(word in user_input for word in ['anger', 'irritate', 'angry']):
        return "anger"
    
    else:
        return "neutral"