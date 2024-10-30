import os
from gtts import gTTS
from tqdm import tqdm

def text_to_speech(text, output_dir="output", filename="narration.mp3"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, filename)
    
    sentences = text.split('. ')
    
    for sentence in tqdm(sentences, desc="Processing Sentences", unit="sentence"):
        tts = gTTS(text=sentence, lang='en')
        tts.save(file_path)

    print(f"Audio saved to: {file_path}")
