from flask import Flask, render_template, jsonify, request
from breathing_monitor import detect_exhale
from audio_engine import listen_and_analyze
from brain import analyze_stress

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start_breathing_monitor", methods=["POST"])
def start_breathing_monitor():
    # 1. Listen (Gets both Text and RMS volume)
    audio_data = listen_and_analyze()

    # 2. Analyze (Checks both)
    result = analyze_stress(audio_data)

    return jsonify(result)

@app.route("/start_breathing_exercise", methods=["POST"])
def start_breathing_exercise():
    detect_exhale(duration=10)
    return jsonify({"status": "Breathing exercise completed"})

if __name__ == "__main__":
    app.run(debug=True)