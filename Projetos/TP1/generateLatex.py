from info import FILES, openJson, openFileWrite

def escape_latex(text):
    """Escapa caracteres especiais para LaTeX"""
    specials = ['\\', '&', '%', '$', '#', '_', '{', '}', '~', '^']
    for s in specials:
        text = text.replace(s, '\\' + s)
    return text

def generate_latex(file_name, top_sentences, entities, source_url):
    latex = ""

    latex += "\\documentclass{article}\n"
    latex += "\\usepackage[utf8]{inputenc}\n"
    latex += "\\usepackage[brazil]{babel}\n"
    latex += "\\usepackage{hyperref}\n"
    latex += "\\usepackage{geometry}\n"
    latex += "\\geometry{margin=2cm}\n\n"

    latex += f"\\title{{Resumo - {escape_latex(file_name)}}}\n"
    latex += "\\author{Guilherme}\n"
    latex += "\\date{\\today}\n\n"

    latex += "\\begin{document}\n"
    latex += "\\maketitle\n\n"

    latex += "\\begin{abstract}\n"
    for s, score in top_sentences.items():
        print(s)
        latex += f"{escape_latex(s)} (Score: {score:.4f})\n\n"
    latex += "\\end{abstract}\n\n"

    latex += "\\section{Entidades Nomeadas}\n"
    latex += "\\begin{itemize}\n"
    for ent, label in entities.items():
        latex += f"\\item \\textbf{{{escape_latex(str(ent))}}} ({escape_latex(str(label))})\n"
    latex += "\\end{itemize}\n\n"

    latex += "\\section{Bibliografia}\n"
    latex += "\\begin{itemize}\n"
    latex += f"\\item \\url{{{source_url}}}\n"
    latex += "\\end{itemize}\n\n"

    latex += "\\end{document}"

    return latex


info = openJson("infoFiles/Spacy.json")
frases = openJson("infoFiles/top3Frases.json")

for key, file in FILES.items():
    if file['metodo'] == "pdf":
        latex_code = generate_latex(key, frases[key], info[key], file['id'])
    else:
        latex_code = generate_latex(key, frases[key], info[key], file['url'])
    
    openFileWrite(f"latexFiles/{key}.tex", latex_code)