import os
import time
from nltk.tokenize import sent_tokenize
from narrate import text_to_speech
from video import generate_video
from parse import extract_text_from_pdf
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def groq_summarize(text):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"You are a helpful assistant that summarizes academic texts into gen-z language. Jump directly to the topic, do not mention the instruction. Summarize within 5 sentences only: {text}"
            }
        ],
        
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content.strip()  # Return the summary

def summarize_text(text):
    sentences = sent_tokenize(text)
    max_chunk_size = 1500
    overlap_size = 3
    chunks = []
    current_chunk = []

    for sentence in sentences:
        if len(" ".join(current_chunk)) + len(sentence) <= max_chunk_size:
            current_chunk.append(sentence)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = current_chunk[-overlap_size:] + [sentence]
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    summaries = []
    for idx, chunk in enumerate(chunks):
        summary = groq_summarize(chunk)
        summaries.append(summary)

        print(f"Processed chunk {idx + 1}/{len(chunks)}")

    combined_summary = " ".join(summaries)
    return combined_summary

if __name__ == "__main__":
    pdf_path = "./data/sample.pdf"
    extracted_text = extract_text_from_pdf(pdf_path)

    if extracted_text.strip():
        start_time = time.time()
        summary = summarize_text(extracted_text)
        text_to_speech(summary, output_dir="./output/audio", filename="narration.mp3")
        generate_video(summary)        
        end_time = time.time()

        print("Summary:\n", summary)
        print(f"Overall time taken: {end_time - start_time:.2f} seconds")
    else:
        print("No text extracted from the PDF.")
