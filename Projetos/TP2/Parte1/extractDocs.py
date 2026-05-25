import wikipediaapi
import json

# Configura o User-Agent (exigido pela Wikipédia)
wiki = wikipediaapi.Wikipedia(
    user_agent='MeuProjetoEscolarNLP/1.0 (contacto@email.com)',
    language='pt'
)

# Lista de temas de futebol para pesquisar
temas = [
    "Futebol", "História do futebol", "Regras do futebol", "Copa do Mundo FIFA",
    "Liga dos Campeões da UEFA", "Cristiano Ronaldo", "Lionel Messi", "Pelé",
    "Eusébio", "Estádio da Luz", "Estádio do Dragão", "Estádio José Alvalade",
    "Seleção Portuguesa de Futebol", "Primeira Liga", "Bola de Ouro"
]

corpus = []

for tema in temas:
    page = wiki.page(tema)
    if page.exists():
        # Dividir o texto da página por parágrafos para gerar vários documentos
        paragrafos = page.text.split('\n')
        for p in paragrafos:
            # Filtrar parágrafos muito pequenos ou vazios
            if len(p.strip()) > 100: 
                corpus.append(p.strip())

print(f"Total de documentos recolhidos: {len(corpus)}")

# Garantir que temos pelo menos 100 documentos
corpus = corpus[:100] if len(corpus) >= 100 else corpus


with open('corpus_futebol.json', 'w', encoding='utf-8') as f:
    json.dump(corpus, f, ensure_ascii=False, indent=4)