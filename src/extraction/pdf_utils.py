import pdfplumber

def open_pdf(pdf_path):
    """
    Opens a PDF file using pdfplumber.
    """

    return pdfplumber.open(pdf_path)

def extract_text_range(pdf_path, start_page, end_page):
    """
    Extracts text from a range of pages in a PDF file.
    """
    extracted_text =[]

    with pdfplumber.open(pdf_path) as pdf:
        for page_number in range(start_page, end_page + 1):
            page = pdf.pages[page_number]
            text = page.extract_text()

            if text:
                extracted_text.append(
                    f"\n=== PAGE {page_number + 1} ===\n\n{text}\n"
                )

    return "\n".join(extracted_text)

def extract_words_range(pdf_path, start_page, end_page):
    """
    Extracts words from a range of pages in a PDF file.
    """
    all_words = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number in range(start_page, end_page + 1):
            page = pdf.pages[page_number]
            words = page.extract_words()

            for word in words:
                word["page"] = page_number + 1
                all_words.append(word)

    return all_words            