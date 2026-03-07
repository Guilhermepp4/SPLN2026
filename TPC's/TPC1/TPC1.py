# ler ficheiro
import re

with open("medicina.xml") as f: 
    texto = f.read()
texto = re.sub(r"<b>\s*(\d+) ", r"<b>@@\1 ", texto)

conceito = re.split(r"<b>\s*@", texto)

def processar_conceito(c):
    # extrair
    id = re.search(r"^@(\d+)", c)
    c = re.sub(r"SIN\.-", r"@SIN.-", c)
    c = re.sub(r"VAR\.-", r"@VAR.-", c)
    c = re.sub(r"Nota\.-", r"@Nota.-", c)

    sin = re.search(r"@SIN\.-([^@<]+)", c)
    var = re.search(r"@VAR\.-([^@<]+)", c)
    nota = re.search(r"@Nota\.-([^@<]+)", c)
    
    blocos = re.findall(
        r'>\s*(en|pt|es|la)\s*</text>\n(.*?)(?=>[ ]*(en|pt|es|la)\s*</text>|<b>)',
        c,
        re.DOTALL
    )
    for lang, bloco, _ in blocos:
        ling = [(lang, ' '.join(t for t in re.findall(r"<i>([^<]+)", bloco)))]

    ling = [(lang, ' '.join(t.strip() for t in re.findall(r'<i>([^<]+)', bloco)).strip())
        for lang, bloco, _ in blocos]
    trGal = re.search(r"^@\d+([\w ]+)</b>", c)
    dom = re.search(r"font=\"6\"><i>(.*)</i>", c)

    res = {}

    if not id:
        return {}, None
    if nota:
        res["nota"] = nota.group(1)
    if var:
        res["var"] = var.group(1)
    if sin:
        res["sin"] = sin.group(1)
    if trGal:
        res["galego"] = trGal.group(1)
    if dom:
        res["dom"] = dom.group(1)

    for l, t in ling:
        res[l] = t

    return res, id.group(1)

entries = {}
for c in conceito[1:]:
    res, id = processar_conceito(c)
    entries[id] = res

import json
f_out = open("dicionario_mediciona.json", "w")
json.dump(entries, f_out, indent=4, ensure_ascii=False)