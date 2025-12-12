from flask import Flask, render_template, jsonify, request
from breathing_monitor import detect_exhale
from audio_engine import listen_and_analyze
from brain import ask_brain
from tts_engine import speak_text # Import the new TTS function
import time
import db_manager

app = Flask(__name__)

# Global state to track grounding (0 = off)
grounding_stage = 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start_breathing_monitor", methods=["POST"])
def start_breathing_monitor():
    global grounding_stage
    grounding_stage = 0 # Reset on new regular check

    audio_data = listen_and_analyze()
    result = analyze_stress(audio_data)

    intensity_score = 2
    emotion_label = "Calm"
    # CHECK FOR PANIC TRIGGER
    # If brain.py says "panic" (we will update brain.py next), start grounding.
    if result.get("stress") == "high":
        intensity_score = 8
        emotion_label = "High Stress"
    elif result.get("stress") == "critical":
        intensity_score = 10
        emotion_label = "Panic"
    elif result.get("stress") == "low":
        intensity_score = 2
        emotion_label = "Calm"

    db_manager.log_stress(emotion_label, intensity_score)

    if result.get("status") == "PANIC_ATTACK":
        grounding_stage = 1
        return jsonify({
            "status": "PANIC_ATTACK",
            "stress": "critical",
            "action": "start_grounding"
        })
    
    return jsonify(result)

@app.route("/perform_grounding_step", methods=["POST"])
def perform_grounding_step():
    """
    Handles the 5-4-3-2-1 technique logic loop.
    """
    global grounding_stage
    data = request.json
    client_stage = data.get('stage', 1)
    
    # Update global stage (safety sync)
    grounding_stage = client_stage

    prompts = {
        1: "I sense high anxiety. Let's ground ourselves. Name 5 things you can see around you.",
        2: "Great job. Now, tell me 4 things you can touch.",
        3: "You are doing well. Name 3 things you can hear.",
        4: "Almost there. Name 2 things you can smell.",
        5: "Last one. Name 1 thing you can taste or 1 good thing about yourself."
    }

    if grounding_stage > 5:
        speak_text("You did great. Returning to normal monitoring.")
        return jsonify({"completed": True, "message": "Exercise Complete"})

    # 1. SPEAK THE INSTRUCTION
    current_prompt = prompts.get(grounding_stage, "")
    print(f"Server Speaking: {current_prompt}")
    speak_text(current_prompt)
    
    # Wait a moment for TTS to start/finish before listening
    # (Adjust this sleep based on prompt length if needed, or rely on UI delay)
    time.sleep(4) 

    # 2. LISTEN FOR USER RESPONSE
    # We use a longer timeout here because users need time to think/look around
    audio_data = listen_and_analyze() 
    user_text = audio_data.get("text", "")

    # 3. VERIFY RESPONSE (Simple Word Count)
    # We split by spaces to approximate the "count" of items
    word_count = len(user_text.split()) if user_text else 0
    
    print(f"Stage {grounding_stage} | User said: {user_text} | Count: {word_count}")

    # Logic: Did they say enough? (We are lenient, just checking if they spoke something)
    if word_count > 0:
        feedback = "Good."
        next_stage = grounding_stage + 1
    else:
        feedback = "I didn't hear you. Let's try again."
        next_stage = grounding_stage # Repeat same stage
        speak_text("I didn't catch that. Please try again.")

    return jsonify({
        "completed": False,
        "current_stage": grounding_stage,
        "next_stage": next_stage,
        "user_said": user_text,
        "feedback": feedback
    })

@app.route("/conversation_turn", methods=["POST"])
def conversation_turn():
    """
    1. Listen to User (Mic)
    2. Send text to Brain (AI)
    3. Speak response (TTS)
    """
    # 1. LISTEN
    print("--- [Conversation Turn] Listening... ---")
    data = listen_and_analyze() # Uses your existing audio engine
    user_text = data.get("text", "")
    
    if not user_text:
        return jsonify({"status": "silence", "reply": ""})

    # 2. THINK (AI)
    print(f"--- [User Said] {user_text} ---")
    ai_reply = ask_brain(user_text)

    # 3. SPEAK (TTS)
    # The speak_text function blocks until audio finishes, 
    # so we don't start listening again too early.
    speak_text(ai_reply)

    return jsonify({
        "status": "success", 
        "user_text": user_text, 
        "reply": ai_reply
    })

@app.route("/start_breathing_exercise", methods=["POST"])
def start_breathing_exercise():
    detect_exhale(duration=10)
    return jsonify({"status": "Breathing exercise completed"})

@app.route("/get_history", methods=["GET"])
def get_history():
    """API for Chart.js"""
    data = db_manager.get_recent_history()
    # Format: {"labels": ["10:00", "10:05"], "values": [2, 8]}
    response = {
        "labels": [row[0] for row in data],
        "values": [row[1] for row in data]
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)