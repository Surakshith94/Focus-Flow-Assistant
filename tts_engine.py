from gtts import gTTS
import pygame
import os
import time
import uuid

# Initialize Pygame Mixer
try:
    pygame.mixer.init()
except pygame.error:
    print("Warning: No audio device found.")

def speak_text(text):
    """
    Online Text-to-Speech using Google Translate API (gTTS).
    1. Sends text to Google.
    2. Downloads MP3.
    3. Plays it.
    """
    if not text:
        return

    print(f"🤖 Flow Says: {text}")
    
    # Unique filename to prevent locking errors
    filename = f"google_voice_{uuid.uuid4().hex}.mp3"

    try:
        # 1. Generate (Connects to Google)
        # tld='com' = US English. Try tld='co.uk' or tld='co.in' for different accents.
        tts = gTTS(text=text, lang='en', tld='co.in', slow=False) 
        tts.save(filename)
        
        # 2. Play
        if os.path.exists(filename):
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            
            # Block until finished
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Unload
            pygame.mixer.music.unload()
            
            # 3. Cleanup
            time.sleep(0.1)
            try:
                os.remove(filename)
            except:
                pass

    except Exception as e:
        print(f"TTS Error: {e}")
        # Clean up if it failed
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass

if __name__ == "__main__":
    print("Testing Google Voice...")
    speak_text("Hello boss. I am connected to Google servers and ready to help.")