def analyze_stress(text_input):
    """
    Analyzes the given text input for stress indicators.
    
    Parameters:
    text_input (str): The text to be analyzed.
    
    Returns:
    dict: A dictionary containing stress analysis results.
    """
    stress_indicators = ['anxious', 'stressed', 'overwhelmed', 'nervous', 'tense']
    analysis_result = {
        'stress_level': 0,
        'indicators_found': []
    }
    
    words = text_input.lower().split()
    for word in words:
        if word in stress_indicators:
            analysis_result['stress_level'] += 1
            analysis_result['indicators_found'].append(word)
    
    return analysis_result

if __name__ == "__main__":
    sample_text = "I have been feeling very anxious and overwhelmed lately."
    result = analyze_stress(sample_text)
    print("Stress Analysis Result:", result)