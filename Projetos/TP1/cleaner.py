import re

def cleanText(text, id):

    if id == "PDFPauloDias":
        text = text.replace('\f', '')
        text = re.sub(r'-\n', '-', text)
        text = re.sub(r'\n(?=[a-zà-ú])', ' ', text)
        text = re.sub(r'\[\d+\]', '', text)
        text = re.sub(r'[A-Z][a-z]+, .*?\d{4}.*?\.', '', text)
        text = re.sub(r'^\d+\.\s+[A-Z].*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n{2,}', '\n\n', text)
    
    elif id == 'PDFOliveiraMartins':
        text = text.replace('\f', '')
        text = re.sub(r'\[\d+\].*', '', text)
        text = re.sub(r'Título:.*?ISBN:.*?\n', '', text, flags=re.DOTALL)
        text = re.sub(r'LIVRO [A-Z]+.*?(?=CAPÍTULO|Nas|A |O )', '', text, flags=re.DOTALL)
        text = re.sub(r'\n(?=[a-zà-ú])', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n{2,}', '\n\n', text)
    
    else:
        text = re.sub(r' ([,;:\.\!\?])', r'\1', text)
        text = re.sub(r'\[\d+\]', '', text)

    return text