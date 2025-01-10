from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text(text: str, chunk_size=1000, chunk_overlap=200) -> list:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_text(text)
