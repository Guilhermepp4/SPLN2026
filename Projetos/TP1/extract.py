import subprocess
import re
import string
import requests
from bs4 import BeautifulSoup
from info import FILES, openFileRead, openFileWrite
from cleaner import cleanText

def run_pdftotext(pdf_path, txt_path, start_page):
    """Executa o pdftotext no PDF e cria o TXT automaticamente"""
    cmd = ["pdftotext"]

    cmd.append("-layout")
    cmd.extend(["-f", str(start_page)])
    cmd.extend([pdf_path, txt_path])
    
    subprocess.run(cmd, check=True)
    print(f"PDF extraído para {txt_path}")

def run_webtotext(url, headers):
    html_doc = requests.get(url, headers=headers)
    soup = BeautifulSoup(html_doc.text, 'html.parser')

    history_div = soup.find('div', {"class": "mw-content-ltr"})
    paragraphs = history_div.find_all("p")

    text = ""
    for p in paragraphs:
        text += p.text+" "
    print(f"Texto WEB extraído com sucesso")
    return text

def clean_text(text, id):
    """Função de limpeza básica"""
    text = text.lower()
    textClean = cleanText(text, id)
    
    return textClean.strip()

def main():
    for key, file in FILES.items():
        if file['metodo'] == "pdf":
            run_pdftotext(file['id'], file['idSaida'], file['startPage'])

            text = openFileRead(file['idSaida'])
            print(f"Texto extraído tem {len(text)} caracteres")

            cleaned = clean_text(text, key)
        
        else:
            text = run_webtotext(file['url'], file['headers'])
            print(f"Texto extraído tem {len(text)} caracteres")

            cleaned = clean_text(text, key)


        openFileWrite(file['idCleaned'], cleaned)

if __name__ == "__main__":
    main()