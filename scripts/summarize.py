import os, time
from transformers import pipeline
from nltk.tokenize import sent_tokenize
from narrate import text_to_speech
from video import generate_video
from parse import extract_text_from_pdf

os.environ["TOKENIZERS_PARALLELISM"] = "false"
summarizer = pipeline("summarization", model="google/pegasus-large", device=0)
rewriter = pipeline("text2text-generation", model="t5-small", device=0)

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
        max_length = min(int(0.4 * len(chunk.split())), 250)
        min_length = max(int(0.2 * len(chunk.split())), 50)
        if min_length >= max_length:
            min_length = int(0.5 * max_length)

        prompt = ("Summarize the following academic content in a conversational tone, "
                  "retaining sections on main contributions, methodology, and findings.")

        full_input = f"{prompt}\n\n{chunk}"

        summary = summarizer(full_input, max_length=max_length, min_length=min_length, do_sample=False)
        summaries.append(summary[0]['summary_text'].strip())

        print(f"Processed chunk {idx + 1}/{len(chunks)} with max_length={max_length}, min_length={min_length}")

    combined_summary = " ".join(summaries)
    return combined_summary


if __name__ == "__main__":
    pdf_path = "./data/sample.pdf"
    extracted_text = extract_text_from_pdf(pdf_path)

    if extracted_text.strip():
        start_time = time.time()
        summary = summarize_text(extracted_text)

        generate_video(summary)
        text_to_speech(summary, output_dir="./output/audio", filename="narration.mp3")
        
        end_time = time.time()

        print("Summary:\n", summary)
        print(f"Overall time taken: {end_time - start_time:.2f} seconds")
    else:
        print("No text extracted from the PDF.")
