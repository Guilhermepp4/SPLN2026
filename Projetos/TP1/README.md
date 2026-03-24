# 📚 SPLN TP1 – Processamento de Texto e Análise

## 👤 Autor
Guilherme Pinto Pinho

## 📌 Descrição do Projeto
Este projeto foi desenvolvido no âmbito da unidade curricular de SPLN e tem como objetivo processar texto proveniente de diferentes fontes (PDF e Web), aplicando técnicas de NLP (Natural Language Processing), nomeadamente:

- Extração e limpeza de texto
- Tokenização
- Construção de modelos de N-gramas
- Scoring de frases
- Seleção das frases mais relevantes (Top 3)
- Reconhecimento de Entidades Nomeadas (NER) com spaCy
- Geração automática de artigos em LaTeX

---

## 📂 Estrutura do Projeto

```
├── extract.py # Extração e limpeza dos textos
├── tokenizar.py # Tokenização + modelo N-gram + scoring
├── NER.py # Identificação de entidades com spaCy
├── generateLatex.py # Geração dos artigos LaTeX
├── cleaner.py # Funções de limpeza
├── info.py # Funções auxiliares e info das fontes
├── TXTfiles # Pasta com a informação extraída
├── PDFFiles # Pasta com os ficheiros PDF originais
├── latexFiles # Pasta com os ficheiros .tex
├── infoFiles # pasta com os ficheiros json de suporte
├── FPDFfiles # pasta com os ficheiros finais em PDF
└── Cleanfiles # pasta com os ficheiros após a limpeza
```
---

## ⚙️ Funcionalidades

### 🔹 1. Extração e Limpeza
- Remove ruído dos PDFs (headers, referências, etc.)
- Limpeza específica para cada fonte

### 🔹 2. Tokenização
- Conversão do texto em tokens
- Construção do vocabulário

### 🔹 3. Modelo N-gram
- Criação de modelo baseado em N-gramas
- N definido pelo utilizador

### 🔹 4. Scoring de Frases
- Cada frase recebe um score baseado na probabilidade dos seus N-gramas
- Uso de **log-probabilidades com smoothing (Laplace)**

### 🔹 5. Seleção das Melhores Frases
- Escolha das **Top 3 frases mais relevantes**
- Baseado no score calculado

### 🔹 6. NER (Named Entity Recognition)
- Uso da biblioteca **spaCy**
- Identificação de:
  - Pessoas
  - Locais
  - Organizações
  - Datas
  - etc...

### 🔹 7. Geração de LaTeX
- Criação automática de artigos com:
  - Abstract (Top 3 frases)
  - Lista de entidades nomeadas
  - Bibliografia

---

## ▶️ Como Executar

### 1️⃣ Instalar dependências

```bash
pip install nltk spacy
python -m spacy download pt_core_news_sm
python3 main.py