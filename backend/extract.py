import pdfplumber
import re

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def extract_info(text):
    name_match = re.search(r"Name:\s*(.+)", text)
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    phone_match = re.search(r"\b\d{10}\b", text)
    skills_match = re.findall(r"\b(Java|Python|React|SQL|C\+\+|AWS)\b", text, re.IGNORECASE)

    return {
        "name": name_match.group(1) if name_match else "Unknown",
        "email": email_match.group() if email_match else "Unknown",
        "phone": phone_match.group() if phone_match else "Unknown",
        "core_skills": list(set(skills_match)) if skills_match else [],
    }
