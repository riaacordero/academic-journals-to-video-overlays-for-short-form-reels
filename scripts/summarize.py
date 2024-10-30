import os, time
from transformers import pipeline
from nltk.tokenize import sent_tokenize

os.environ["TOKENIZERS_PARALLELISM"] = "false"
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=0)
rewriter = pipeline("text2text-generation", model="t5-small", device=0)

def summarize_text(text, max_length=250, min_length=50):

    # Sentence tokenizer
    sentences = sent_tokenize(text)

    max_chunk_size = 1024
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_size:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence  # Start a new chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    summaries = []
    total_time = 0.0

    for idx, chunk in enumerate(chunks):
        start_time = time.time()
        # Prompt engineering goes here:
        prompt = (f"Summarize the following academic text into three concise paragraphs. "
                  f"Focus on the main contributions, methodology, and findings:"f"\n\n{chunk}")
        summary = summarizer(prompt, chunk, max_length=max_length, min_length=min_length, do_sample=False)
        end_time = time.time()

        chunk_summary = summary[0]['summary_text']
        summaries.append(chunk_summary)

        chunk_time = end_time - start_time
        total_time += chunk_time
        print(f"Processed chunk {idx + 1}/{len(chunks)} in {chunk_time:.2f} seconds.")

    print(f"Total time for summarization: {total_time:.2f} seconds.")
    return " ".join(summaries)


def rewrite_text(summary, max_length=150):
    # Prompt for rewriting
    prompt = f"Rewrite the text in a conversational tone. Keep it up to a paragraph long\n\n{summary}"
    rewritten = rewriter(prompt, max_length=max_length, do_sample=False)
    return rewritten[0]['generated_text']


if __name__ == "__main__":
    from parse import extract_text_from_pdf
    
    pdf_path = "./data/paper/sample.pdf"
    extracted_text = extract_text_from_pdf(pdf_path)
    
    if extracted_text.strip():
        start_time = time.time()
        summary = summarize_text(extracted_text)
        rewritten_summary = rewrite_text(summary)
        end_time = time.time()
        
        print("Summary:\n", summary)
        print("Rewritten Summary:\n", rewritten_summary)
        print(f"Overall time taken: {end_time - start_time:.2f} seconds")
    else:
        print("No text extracted from the PDF.")
