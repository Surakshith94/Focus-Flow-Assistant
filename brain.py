def analyze_stress(data):
    text = data.get('text', '').lower()
    rms = data.get('rms', 0)

    # CRITICAL FIX: Calibrated to your logs (Your heavy breathing is ~130)
    LOUDNESS_THRESHOLD = 80
    
    # Words that trigger stress even if you are whispering
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

    # 1. Check Volume (Breathing)
    if rms > LOUDNESS_THRESHOLD:
        analysis_result['stress'] = 'high'
        analysis_result['status'] = f'Heavy Breathing Detected (Vol: {rms})'

    # 2. Check Words (Overrides volume)
    for word in STRESS_KEYWORDS:
        if word in text:
            analysis_result['stress'] = 'high'
            analysis_result['status'] = f'Distress Signal: "{word}"'
            break
            
    return analysis_result