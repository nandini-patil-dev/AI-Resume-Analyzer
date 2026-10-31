
from pypdf import PdfReader

def extract_resume_text(pdf_file):

    # Extract readable text from an uploaded PDF resume.


    reader = PdfReader(pdf_file)

    extracted_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            extracted_text += text + "\n"

    return extracted_text
