import speech_recognition as sr

def listen_to_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Adjust for ambient noise before listening
        print("Adjusting for ambient noise... Please wait.")
        
        print("Listening...")
        audio_data = recognizer.listen(source)
        
        try:
            text = recognizer.recognize_google(audio_data)
            print("You said: " + text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            return None

if __name__ == "__main__":
    listen_to_audio()