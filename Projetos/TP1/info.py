import json

FILES = {
    "PDFPauloDias": {
        "id": "PDFfiles/CHAM_Paulo_Dias_Fiogo_Ferreira_embargo_18_meses.pdf",        
        "idSaida": "TXTfiles/CHAM_Paulo_Dias_Fiogo_Ferreira_embargo_18_meses.txt",
        "startPage": 20,
        "idCleaned": "Cleanfiles/CHAM_Paulo_Dias_Fiogo_Ferreira_embargo_18_meses_Clean.txt",
        "metodo": "pdf"
    },
    "PDFOliveiraMartins": {
        "id": "PDFfiles/Historia de Portugal_ Tomo I - Oliveira Martins.pdf",        
        "idSaida": "TXTfiles/Historia de Portugal_ Tomo I - Oliveira Martins.txt",
        "startPage": 5,
        "idCleaned": "Cleanfiles/Historia de Portugal_ Tomo I - Oliveira Martins.txt",
        "metodo": "pdf"
    },
    "WEBPAGE1": {
        "url": "https://pt.wikipedia.org/wiki/História_de_Portugal",        
        "headers": {"User-Agent" : "Mozilla/5.0"},
        "idCleaned": "Cleanfiles/wikepediaHistoria.txt",
        "metodo": "web"
    }
}

def openFileRead(path):
    with open(path, "r", encoding="UTF-8") as f:
        return f.read()
    
def openFileWrite(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def openJson(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)