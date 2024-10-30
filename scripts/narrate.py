import pyttsx3

def text_to_speech(text, filename="narration.mp3"):
    engine = pyttsx3.init()
    
    # TTS Properties
    engine.setProperty('rate', 150)  # speed
    engine.setProperty('volume', 1)  # loudness
    
    engine.save_to_file(text, filename)
    
    engine.runAndWait()
