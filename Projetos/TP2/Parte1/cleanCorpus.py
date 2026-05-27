import json
import re

with open("docs/corpus_futebol.json", "r", encoding="utf-8") as f:
    corpus = json.load(f)

corpus_limpo = []

print(f"A iniciar a limpeza de {len(corpus)} documentos...")

for doc in corpus:
    paragrafos_limpos = []
    
    for p in doc["text"]:
        texto = re.sub(r'\[\d+\]', '', p)          # Remove [1], [2], etc.
        texto = re.sub(r'\[nota \d+\]', '', texto)  # Remove [nota 1], etc.
        texto = re.sub(r'\[\w+\]', '', texto)       # Remove outras tags entre colchetes
        
        texto = re.sub(r'\s+', ' ', texto).strip()
        
        # C. Filtrar parágrafos que ficaram vazios ou demasiado pequenos após a limpeza
        # Parágrafos com menos de 40 caracteres costumam ser títulos perdidos ou lixo
        if len(texto) > 40:
            paragrafos_limpos.append(texto)
            
    # Só guardamos o documento se ele ainda contiver parágrafos válidos com texto real
    if len(paragrafos_limpos) > 0:
        doc_atualizado = {
            "id": doc["id"],
            "title": doc["title"],
            "text": paragrafos_limpos,
            "url": doc["url"]
        }
        corpus_limpo.append(doc_atualizado)

print(f"Limpeza concluída! Permaneceram {len(corpus_limpo)} documentos válidos.")

with open("docs/corpus_futebol_limpo.json", "w", encoding="utf-8") as f:
    json.dump(corpus_limpo, f, ensure_ascii=False, indent=2)

print("O teu corpus limpo foi guardado em 'corpus_futebol_limpo.json'.")