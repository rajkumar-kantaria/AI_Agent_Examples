from typing import List
import PyPDF2
from utils.text_splitter import split_text

def extract_text_from_pdf(pdf_path: str) -> List[str]:
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return split_text(text)
