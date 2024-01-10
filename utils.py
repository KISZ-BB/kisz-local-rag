import os
from pypdf import PdfReader


def list_files(path, extensions=''):
    """Returns a List of strings with the file names on the given path"""

    files_list = [
        os.path.join(path, f)
        for f in os.listdir(path)
        if os.path.isfile(os.path.join(path, f)) and f.endswith(extensions)
    ]
    return sorted(files_list)


def read_file(doc):
    """Get text from pdf and txt files"""
    text = ''
    if doc.endswith('.txt'):
        with open(doc, 'r') as f:
            text = f.read()
    elif doc.endswith('.pdf'):
        pdf_reader = PdfReader(doc)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_chunks_basic(text, max_words=256):
    """Split text in chunks with less than max_words"""

    # List of lines skipping empty lines
    lines = [l for l in text.splitlines(True) if l.strip()]

    chunks = []
    chunk = ''
    for l in lines:
        if len(chunk.split() + l.split()) <= max_words:
            chunk += l  # if splitline(False) do += "\n" + l
            continue
        chunks.append(chunk)
        chunk = l

    if chunk:
        chunks.append(chunk)

    return chunks


def get_chunks(text, max_words=256, max_title_words=4):
    """Split text in trivial context-awared chunks with less than max_words"""

    # List of lines skipping empty lines
    lines = [l for l in text.splitlines(True) if l.strip()]

    chunks = []
    chunk = ''
    for l in lines:
        nwords = len(l.split())
        if len(chunk.split()) + nwords <= max_words and (
            nwords >= max_title_words
            or all(len(s.split()) <= max_title_words for s in chunk.splitlines())
        ):
            chunk += l  # if splitline(False) do += "\n" + l
            continue
        chunks.append(chunk)
        chunk = l

    if chunk:
        chunks.append(chunk)

    return chunks


if __name__ == '__main__':
    # check chunk splitting
    docs_path = 'data'
    files = list_files(docs_path, extensions=('.txt', '.pdf'))
    print(files)
    text = read_file(files[0])
    chunks = get_chunks(text)
    print("\nChunks:")
    for c in chunks:
        print(c)
        print("Words Length:", len(c.split()))
        print(80 * '-')
