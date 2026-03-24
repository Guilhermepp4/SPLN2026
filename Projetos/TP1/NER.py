import spacy
from info import FILES, openFileRead
from collections import defaultdict

nlp = spacy.load("pt_core_news_sm")

res = {}
for key, file in FILES.items():
    text = openFileRead(file['idCleaned'])

    doc = nlp(text)

    entities_by_type = defaultdict(list)
    for ent in doc.ents:
        entities_by_type[ent.label_].append(ent.text)
    
    res[key] = dict(entities_by_type)

import json
f_out = open("infoFiles/Spacy.json", "w")
json.dump(res, f_out, indent=4, ensure_ascii=False)