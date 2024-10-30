import os, time
from transformers import pipeline
from nltk.tokenize import sent_tokenize

os.environ["TOKENIZERS_PARALLELISM"] = "false"
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=0)
rewriter = pipeline("text2text-generation", model="t5-small", device=0)

def summarize_text(text, max_length=250, min_length=50):
    sentences = sent_tokenize(text)

    # Adjust chunk size to the model's capacity
    max_chunk_size = 1024
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_size:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    summaries = []
    for idx, chunk in enumerate(chunks):
        input_length = len(chunk.split())
        max_length = min(int(0.4 * input_length), max_length) 
        min_length = max(int(0.2 * input_length), min_length)

        if min_length >= max_length:
            min_length = int(0.5 * max_length)

        summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
        summaries.append(summary[0]['summary_text'])
        print(f"Processed chunk {idx + 1}/{len(chunks)}")

    combined_summary = " ".join(summaries)
    return combined_summary


def rewrite_text(summary, max_length=150):
    # Prompt for rewriting
    prompt = f"Rewrite the text in a conversational tone. Keep it up to a paragraph long\n\n{summary}"
    rewritten = rewriter(prompt, summary, max_length=max_length, do_sample=False)
    return rewritten[0]['generated_text']


if __name__ == "__main__":
    from parse import extract_text_from_pdf
    
    pdf_path = "./data/paper/sample.pdf"
    extracted_text = extract_text_from_pdf(pdf_path)
    
    if extracted_text.strip():
        start_time = time.time()
        
        summary = summarize_text(extracted_text)
        print("Initial Summary:\n", summary)

        rewritten_summary = rewrite_text(summary)
        print("Rewritten Summary:\n", rewritten_summary)

        end_time = time.time()
        print(f"Overall time taken: {end_time - start_time:.2f} seconds")

    else:
        print("No text extracted from the PDF.")