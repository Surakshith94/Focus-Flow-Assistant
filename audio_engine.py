import speech_recognition as sr
import audioop

def listen_and_analyze():
    recognizer = sr.Recognizer()
    
    # CRITICAL FIX: Set threshold EXTREMELY low (50).
    # This ensures it captures YOUR quiet mic and doesn't "Time Out".
    recognizer.energy_threshold = 50
    recognizer.dynamic_energy_threshold = False  

    with sr.Microphone() as source:
        print(f"Microphone active (Sensitivity: High). Listening...")
        
        try:
            # timeout=None means "wait forever until sound starts" (but since threshold is 50, it starts instantly)
            # phrase_time_limit=5 means "record for 5 seconds max"
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            # 1. Calculate Loudness
            raw_data = audio.get_raw_data()
            rms = audioop.rms(raw_data, 2) 
            print(f" >> Audio Captured. Volume Level: {rms}")

            # 2. Text Recognition
            text = ""
            try:
                # We try to recognize text even if volume is low
                text = recognizer.recognize_google(audio)
                print(f" >> Voice detected: '{text}'")
            except sr.UnknownValueError:
                print(" >> No distinct words (likely just breathing)")
            except sr.RequestError:
                print(" >> API connection error")

            return {"text": text, "rms": rms}

        except sr.WaitTimeoutError:
            print(" >> Still timing out? Try moving closer to the mic.")
            return {"text": "", "rms": 0}
        except Exception as e:
            print(f"Error in audio_engine: {e}")
            return {"text": "", "rms": 0}

if __name__ == "__main__":
    listen_and_analyze()