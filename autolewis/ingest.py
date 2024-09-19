import pypdf
import re

END_OF_DOCUMENT = re.compile("Document [a-zA-Z0-9]{25}")
TRASH_SIGNIFIERS = [re.compile(p) for p in [
    "^Page ?[0-9]{1,4} ?of ?[0-9]{1,4}",
    "^Copyright( ©)? [0-9]{4}",
    "^[0-9,]+ words",
]]

def extract_articles(file: str):
    pdf = pypdf.PdfReader(file)
    content = "\n".join([p.extract_text() for p in pdf.pages])
    articles = []

    current_article = []

    lines = [ln for ln in content.splitlines() if not any([s.search(ln) for s in TRASH_SIGNIFIERS])]
    for line in lines:
        if line.startswith("Document") and END_OF_DOCUMENT.search(line):
            articles.append("\n".join(current_article))
            current_article = []
            continue
        if line:
            current_article += [line]
    return articles
