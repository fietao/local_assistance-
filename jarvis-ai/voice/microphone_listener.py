import speech_recognition as sr
import pyttsx3
import threading

class VoiceIntegration:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        """Speaks the given text out loud using the local TTS engine. 
        Runs in a background thread to prevent blocking the FastApi server."""
        def _speak():
            try:
                # Re-initialize engine internally for the thread to avoid COM context issues on Windows
                engine = pyttsx3.init()
                engine.setProperty('rate', 170)  # slightly slower, more natural speed
                voices = engine.getProperty('voices')
                
                # Pick a female voice if available (commonly Zira on Windows)
                for voice in voices:
                    if "zira" in voice.name.lower() or "female" in voice.name.lower():
                        engine.setProperty('voice', voice.id)
                        break
                        
                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                print(f"Voice engine failed: {e}")
                
        threading.Thread(target=_speak, daemon=True).start()

    def listen(self):
        """Listens to the default local computer microphone and transcribes speech to text."""
        with sr.Microphone() as source:
            print("[Voice] Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("[Voice] Listening to physical microphone now...")
            
            try:
                # Listen to the user's voice (times out if no speech detected)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=15)
                print("[Voice] Audio captured. Transcribing...")
                
                # Convert the audio to text
                text = self.recognizer.recognize_google(audio)
                return text
                
            except sr.WaitTimeoutError:
                return "(Silence)"
            except sr.UnknownValueError:
                return "(Could not understand audio)"
            except sr.RequestError as e:
                return f"(Speech Recognition API Error: {e})"

voice = VoiceIntegration()