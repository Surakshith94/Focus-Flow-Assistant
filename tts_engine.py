import pyttsx3
import threading

def speak_text(text):
    """
    Uses pyttsx3 to speak the text. 
    We run this in a separate thread so it doesn't freeze the Flask app.
    """
    def _run():
        try:
            engine = pyttsx3.init()
            # Optional: Adjust rate (speed) and volume
            engine.setProperty('rate', 150) 
            engine.setProperty('volume', 0.9)
            
            # Select a voice (0 is usually male, 1 is usually female)
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id) # Try changing index to 0 for male
            
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")

    # Run in thread so the UI doesn't hang while waiting for the voice to finish
    thread = threading.Thread(target=_run)
    thread.start()