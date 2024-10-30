import fitz

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    
    # Extract text from each page
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text("text") + "\n"
    
    doc.close()
    return text.strip()

if __name__ == "__main__":
    pdf_path = "./data/paper/sample.pdf"
    extracted_text = extract_text_from_pdf(pdf_path)
    print("Extracted Text:\n", extracted_text[:1000])
