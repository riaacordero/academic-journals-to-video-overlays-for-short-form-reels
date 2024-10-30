import pyttsx3
import os

def text_to_speech(text, output_dir="audio_files", filename="narration.mp3"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_path = os.path.join(output_dir, filename)

    engine = pyttsx3.init()
    
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)
    
    engine.save_to_file(text, file_path)
    engine.runAndWait()
    
    print(f"Audio saved to: {file_path}")

# Example usage
if __name__ == "__main__":
    sample_text = "This is a test narration for the text-to-speech conversion."
    text_to_speech(sample_text)
