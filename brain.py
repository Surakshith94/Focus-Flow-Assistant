def analyze_stress(data):
    text = data.get('text', '').lower()
    rms = data.get('rms', 0)

    # CRITICAL KEYWORDS -> TRIGGER GROUNDING
    # If these are heard, we send "PANIC_ATTACK" to app.py
    PANIC_KEYWORDS = ['panic attack', 'can\'t breathe', 'dying', 'heart attack', 'help me']

    for word in PANIC_KEYWORDS:
        if word in text:
            return {
                'stress': 'critical',
                'status': 'PANIC_ATTACK',
                'transcription': text
            }
            
    # CRITICAL SAFETY CHECK (For the Help/WhatsApp buttons)
    CRITICAL_KEYWORDS = ['suicide', 'kill myself', 'end it all']
    for word in CRITICAL_KEYWORDS:
        if word in text:
            return {'stress': 'critical', 'status': 'CRITICAL_ALERT', 'transcription': text}

    # Standard Logic
    LOUDNESS_THRESHOLD = 80
    STRESS_KEYWORDS = ['anxious', 'stressed', 'overwhelmed', 'nervous', 'scared']

    analysis_result = {
        'stress': 'low', 
        'status': 'System Nominal', 
        'transcription': text if text else "..."
    }

    if rms > LOUDNESS_THRESHOLD:
        analysis_result['stress'] = 'high'
        analysis_result['status'] = f'Heavy Breathing (Vol: {rms})'

    for word in STRESS_KEYWORDS:
        if word in text:
            analysis_result['stress'] = 'high'
            analysis_result['status'] = f'Distress Signal: "{word}"'
            break
            
    return analysis_result