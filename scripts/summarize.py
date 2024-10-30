import os
import time
from transformers import pipeline

os.environ["TOKENIZERS_PARALLELISM"] = "false"
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=0)

def summarize_text(text, max_length=250, min_length=50):
    max_chunk_size = 1024
    chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]
    
    summaries = []
    total_time = 0.0

    # Chunking process
    for idx, chunk in enumerate(chunks):
        start_time = time.time()

        # Prompt engineering goes here:
        prompt = (f"Summarize the following academic text into three concise paragraphs. "
                  f"Focus on the main contributions, methodology, and findings:\n\n{chunk}")
        
        summary = summarizer(prompt, max_length=max_length, min_length=min_length, do_sample=False)
        end_time = time.time()

        chunk_summary = summary[0]['summary_text']
        summaries.append(chunk_summary)

        chunk_time = end_time - start_time
        total_time += chunk_time
        print(f"Processed chunk {idx + 1}/{len(chunks)} in {chunk_time:.2f} seconds.")

    print(f"Total time for summarization: {total_time:.2f} seconds.")
    return " ".join(summaries)

if __name__ == "__main__":
    from parse import extract_text_from_pdf
    
    pdf_path = "./data/paper/sample.pdf"
    extracted_text = extract_text_from_pdf(pdf_path)
    
    if extracted_text.strip():
        start_time = time.time()
        summary = summarize_text(extracted_text)
        end_time = time.time()
        
        print("Summary:\n", summary)
        print(f"Overall time taken: {end_time - start_time:.2f} seconds")
    else:
        print("No text extracted from the PDF.")
