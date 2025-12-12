import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
API_KEY = os.getenv("API_KEY")

# --- AI PERSONA ---
# We keep the persona so it stays polite ("Yes boss"), but we allow it to answer ANYTHING.
SYSTEM_PROMPT = """
You are Focus-Flow, a smart and polite AI assistant for an engineering student.
Style: Speak like a respectful junior assistant ('Yes boss', 'Right away', 'Here is the info').
Goal: Answer the user's question accurately, no matter what the topic is (Code, Science, Life, Jokes).
Constraint: Keep answers concise (1-3 sentences) so they are easy to speak out loud.
"""

history = [
    {"role": "user", "parts": ["System Instruction: " + SYSTEM_PROMPT]}
]

# ==========================================
# FUNCTION 1: AI VOICE CHAT (UNRESTRICTED)
# ==========================================
def ask_brain(user_text):
    """
    Sends text to LLM and gets a smart response.
    """
    global history
    history.append({"role": "user", "parts": [user_text]})

    response_text = ""

    # Check for Key
    if not API_KEY:
        return "Boss, I cannot find my API Key. Please check the .env file."

    try:
        # CONFIGURE API
        genai.configure(api_key=API_KEY)
        
        # USE "FLASH" MODEL (Faster, higher limits, smarter)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Generate Response
        chat = model.start_chat(history=history)
        response = chat.send_message(user_text)
        
        response_text = response.text
        
        # Clean up text for speech (remove *stars* or markdown)
        response_text = response_text.replace("*", "").replace("#", "")

    except Exception as e:
        print(f"AI Error: {e}")
        response_text = "I am having trouble connecting to the internet, boss. Please try again."

    # Update Memory
    history.append({"role": "model", "parts": [response_text]})
    
    return response_text


# ==========================================
# FUNCTION 2: BREATHING MONITOR
# ==========================================
def analyze_stress(data):
    """
    Analyzes audio data for stress levels.
    """
    text = data.get('text', '').lower()
    rms = data.get('rms', 0)

    # 1. Panic/Critical Check
    PANIC_KEYWORDS = ['panic attack', 'can\'t breathe', 'dying', 'heart attack', 'help me']
    for word in PANIC_KEYWORDS:
        if word in text:
            return {'stress': 'critical', 'status': 'PANIC_ATTACK', 'transcription': text}
            
    CRITICAL_KEYWORDS = ['suicide', 'kill myself', 'end it all']
    for word in CRITICAL_KEYWORDS:
        if word in text:
            return {'stress': 'critical', 'status': 'CRITICAL_ALERT', 'transcription': text}

    # 2. Standard Stress Check
    LOUDNESS_THRESHOLD = 80
    STRESS_KEYWORDS = ['anxious', 'stressed', 'overwhelmed', 'nervous', 'scared', 'worry']

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