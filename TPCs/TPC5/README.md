# 🧠 TPC 5 — Named Entity Recognition com spaCy

---

## 📌 Objetivo

Este trabalho teve como objetivo treinar um modelo de **Named Entity Recognition (NER)** utilizando a biblioteca spaCy e comparar os resultados com o modelo desenvolvido no exercício da aula.

---

## 📚 Descrição do trabalho

O trabalho foi dividido em duas partes:

1. **Exercício da aula**
   Serviu como base de comparação, já se encontrando previamente funcional.

2. **Treino de modelo com spaCy**
   Consistiu em:

   * Preparar os dados no formato `.iob`
   * Converter os ficheiros para o formato `.spacy`
   * Treinar um modelo de NER
   * Avaliar e comparar os resultados obtidos

---

## 📁 Estrutura do projeto

* `aula_9.ipynb` → Exercício desenvolvido na aula
* `spacy_model.ipynb` → Testes e comandos principais do spaCy
* `arquivo_ner_train.iob` → Dados de treino
* `arquivo_ner_test.iob` → Dados de teste (validação)
* `datasets/` → Dados convertidos para formato `.spacy`
* `output/` → Modelos gerados pelo spaCy (`model-best`, `model-last`)

---

## ⚙️ Comandos utilizados

### 1. Converter dados

```bash
python -m spacy convert -c iob arquivo_ner_train.iob ./datasets
python -m spacy convert -c iob arquivo_ner_test.iob ./datasets
```

### 2. Criar configuração

```bash
python -m spacy init config config.cfg --lang pt --pipeline ner --optimize accuracy
```

### 3. Treinar modelo

```bash
python -m spacy train config.cfg --output ./output \
--paths.train ./datasets/arquivo_ner_train.spacy \
--paths.dev ./datasets/arquivo_ner_test.spacy
```

---

## 📊 Resultados

### 🔹 Modelo da aula

| Epoch | Validation Loss | Precision | Recall   | F1           | Accuracy |
| ----- | --------------- | --------- | -------- | ------------ | -------- |
| 1     | 0.077688        | 0.931162  | 0.959164 | 0.944956     | 0.981128 |
| 2     | 0.068289        | 0.939114  | 0.966762 | **0.952737** | 0.983755 |

👉 Melhor resultado: **F1 = 0.952737**

---

### 🔹 Modelo spaCy

TOK     -    
NER P   99.37
NER R   99.28
NER F   99.33
SPEED   4461 


=============================== NER (per type) ===============================

                  P       R       F
Data          99.79   99.79   99.79
Pessoa        99.46   99.60   99.53
Local         99.73   99.56   99.65
Organizacao   95.96   95.96   95.96
Profissao     96.60   94.67   95.62

---

## ⚖️ Comparação

O modelo treinado com spaCy apresentou melhores resultados

Isto indica uma melhor capacidade de:

* identificar entidades corretamente
* reduzir erros (falsos positivos e negativos)

---

## 🧠 Conclusão

Neste trabalho foi possível treinar um modelo de NER utilizando o spaCy a partir de dados no formato `.iob`.

Após a conversão dos dados e execução do treino, verificou-se que o modelo obtido superou o modelo desenvolvido na aula em todas as métricas avaliadas.

Apesar disso, é importante notar que os resultados dependem fortemente da qualidade e quantidade dos dados utilizados no treino.

---

## 🚀 Notas finais

* O spaCy fornece uma pipeline completa e otimizada para tarefas de NLP
* A conversão correta dos dados é essencial para o sucesso do modelo
* A comparação entre modelos permite avaliar diferentes abordagens e compreender melhor o desempenho obtido

---
