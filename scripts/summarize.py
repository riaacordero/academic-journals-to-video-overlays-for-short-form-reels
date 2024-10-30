from transformers import pipeline

def summarize_text(text, max_length=150, min_length=40):
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']

if __name__ == "__main__":
    from parse import extract_text_from_pdf
    
    # Load extracted text
    pdf_path = "./data/paper/sample.pdf"
    extracted_text = extract_text_from_pdf(pdf_path)
    
    # Summarize the extracted text
    summary = summarize_text(extracted_text)
    print("Summary:\n", summary)
