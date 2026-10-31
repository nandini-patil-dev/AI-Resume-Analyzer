
from resume_parser import extract_resume_text

with open("sample_resume.pdf", "rb") as file:
    text = extract_resume_text(file)

print("Extracted Resume Text:")
print(text)
