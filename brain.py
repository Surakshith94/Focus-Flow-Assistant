def analyze_stress(data):
    text = data.get('text', '').lower()
    rms = data.get('rms', 0)

    # CRITICAL SAFETY CHECK (First Priority)
    CRITICAL_KEYWORDS = ['suicide', 'kill myself', 'end it all', 'no way out', 'want to die']

    for word in CRITICAL_KEYWORDS:
        if word in text:
            # We return a dictionary so the frontend can read it safely
            return {
                'stress': 'critical',
                'status': 'CRITICAL_ALERT',
                'transcription': text
            }

    # --- Standard Stress Logic ---
    LOUDNESS_THRESHOLD = 80
    STRESS_KEYWORDS = [
        'anxious', 'stressed', 'overwhelmed', 'nervous', 'scared', 
        'help', 'panic', 'tension', 'trouble', 'worry'
    ]

    analysis_result = {
        'stress': 'low',
        'status': 'System Nominal',
        'transcription': text if text else "..."
    }

    print(f"Analyzing -> Vol: {rms} | Text: {text}")

    if rms > LOUDNESS_THRESHOLD:
        analysis_result['stress'] = 'high'
        analysis_result['status'] = f'Heavy Breathing Detected (Vol: {rms})'

    for word in STRESS_KEYWORDS:
        if word in text:
            analysis_result['stress'] = 'high'
            analysis_result['status'] = f'Distress Signal: "{word}"'
            break
            
    return analysis_result