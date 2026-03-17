import requests
from bs4 import BeautifulSoup
import json
import string
import time

url_base = "https://www.atlasdasaude.pt"
res = {}
def extrairInf(url):
        soup = BeautifulSoup(url.text, 'html.parser')

        doencas_div = soup.find_all('div', class_='views-row')

        for div in doencas_div:
            nameDoenca = div.div.h3.a.text
            descricaoPeq = div.find('div', class_='views-field-body').div.text
        
            next_url = div.find("h3").a["href"]
            
            fullink = url_base+next_url
            
            page = requests.get(fullink)
            soup2 = BeautifulSoup(page.text, "html.parser")
            
            body = soup2.find("div", class_="field-name-body")

            descricaoGran = ""
            causas = ""
            sintomas = []
            tratamento = ""
            artigosRela = []

            if body:
                section = "descricao"

                for t in body.find_all(["h2", "p", "ul","h3"]):
                    if t.name == "h2":
                        if t.text.lower() == "causas":
                            section = "causas"    
                        elif t.text.lower() == "sintomas":    
                            section = "sintomas"                        
                        elif t.text.lower() == "tratamento":    
                            section = "tratamento"
                        elif t.text.lower() == "artigosRela":
                            section = "artigosRela"
    
                    elif t.name == "p":
                        if section == "descricao":
                            descricaoGran += t.text + " "
                        elif section == "causas":
                            causas += t.text + " "
                        elif section == "tratamento":
                            tratamento += t.text + " "
                        elif section == "sintomas":
                            sintomas.append(t.text)
    
                    elif t.name == "ul":
                        if section == "descricao":
                          descricaoGran = t.li.text + " "
                        elif section == "causas":
                          causas = t.li.text + " "
                        elif section == "tratamento":
                          tratamento = t.li.text + " "
                        elif section == "sintomas":
                            sintomas.append(t.li.text)

                    elif t.name == "h3" and section == "artigosRela":
                        sintomas.append(t.text)
                    
                    # else:
                    #     descricaoGran = body.find('div', class_='field-item').div.text + " "

            res[nameDoenca] = {
                "Descricão Pequena": descricaoPeq,
                "Descricão Grande": descricaoGran,
                "Causas": causas,
                "Sintomas": sintomas,
                "Tratamento": tratamento,
                "Artigos Relacionados": artigosRela
            }

for i in range(ord('a'), ord('z')+1):
    letra = chr(i)
    html_doc = requests.get("https://www.atlasdasaude.pt/doencasaaz/"+letra)
    extrairInf(html_doc)

f_out = open("doencas.json", "w")
json.dump(res, f_out, indent=4, ensure_ascii=False)