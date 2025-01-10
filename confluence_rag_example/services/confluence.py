from typing import List
from bs4 import BeautifulSoup
from atlassian import Confluence
from utils.text_splitter import split_text
from dotenv import load_dotenv
import os

load_dotenv()

def extract_text_from_confluence(pageid: str) -> List[str]:
    
    confluence_url = os.getenv("CONFLUENCE_URL")
    confluence_token = os.getenv("CONFLUENCE_TOKEN")
    if not confluence_token:
        raise ValueError("CONFLUENCE_TOKEN environment variable not found")
    
    confluence = Confluence(
        url=confluence_url,
        username="",
        password=confluence_token
    )
    result = confluence.get_page_as_word(pageid)
    soup = BeautifulSoup(result, features="html.parser")

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    clean_text = '\n'.join(chunk for chunk in chunks if chunk)
    return split_text(clean_text)
