import spacy
import json
import re
import itertools

nlp = spacy.load("pt_core_news_sm")

with open("Harry Potter e A Pedra Filosofal.txt", "r", encoding="utf-8") as f:
    texto = f.read()

doc = nlp(texto)

personagens = {}
combinations = {}
texto_split = re.split(r"\.\s+", texto)

for ent in doc.ents:
    if ent.label_ in ["PER"]:
        if ent.text not in personagens:
            personagens[ent.text] = 0
        personagens[ent.text] += 1


for frase in texto_split:
    for a, b in itertools.combinations(personagens.keys(), 2):
        if a in frase and b in frase:
            pair = tuple(sorted([a,b]))
            if pair not in combinations:
                combinations[pair] = 0
            combinations[pair] += 1


personagens_order = sorted(personagens.items(), key=lambda x: x[1], reverse=True)
print("\n\n________________Personagens________________")
for per in personagens_order[:10]:
    print(f"{per[0]} --> {per[1]}")

combinations_order = sorted(combinations.items(), key=lambda x: x[1], reverse=True)
print("\n\n________________Combinações________________")
for comb in combinations_order[:10]:
    a,b = comb[0]
    print(f"{a} <---> {b} --> {comb[1]}")