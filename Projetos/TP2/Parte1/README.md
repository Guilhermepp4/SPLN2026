# RELATÓRIO TÉCNICO: SISTEMA AVANÇADO DE RETRIEVAL & QUESTION ANSWERING (QA) NO DOMÍNIO DO FUTEBOL

**Unidade Curricular:** Processamento de Língua Natural (SPLN)  
**Curso:** Engenharia de Linguagens / Engenharia Informática  
**Autor:** Guilherme  

---

## 1. Introdução e Contexto
O presente trabalho prático insere-se no âmbito do desenvolvimento de sistemas de Question Answering (QA) aplicados a domínios de conhecimento específicos — neste caso, o futebol mundial. O objetivo principal consistiu em desenhar, implementar e avaliar uma pipeline completa capaz de receber uma pergunta em linguagem natural (Português), vasculhar autonomamente um *corpus* documental extraído da Wikipédia e devolver a resposta correta através de duas abordagens distintas: extrativa e abstractiva.

---

## 2. Processamento e Modelação dos Dados
Antes da aplicação de qualquer algoritmo de inteligência artificial, os dados extraídos da Wikipédia foram submetidos a uma fase crítica de engenharia de dados.

* **Limpeza de Ruído:** Foram removidas *tags* HTML residuais, referências bibliográficas formatadas (ex: `[1]`, `[2]`) e caracteres especiais que pudessem corromper a tokenização.
* **Segmentação Estratégica (Chunking):** Os artigos completos da Wikipédia são longos e ultrapassam frequentemente a janela de contexto máxima (*Context Window*) de modelos baseados em Transformers (como o BERT, limitado a 512 tokens). Para contornar esta restrição, os documentos foram fragmentados e guardados ao nível do **parágrafo independente**, garantindo que cada porção de texto enviada aos modelos continha informação densa e processável sem risco de truncagem.

---

## 3. Arquitetura da Pipeline (Alíneas b, c)
A pipeline foi desenhada seguindo uma arquitetura modular dividida em duas fases principais: **Retrieval** (Recuperação) e **Reading** (Leitura/QA).

### 3.1. O Retriever Configurável e Flexível
O módulo de recuperação de informação (`retriever.py`) foi projetado para oferecer flexibilidade e robustez ao utilizador, permitindo alternar dinamicamente entre três modos de operação:
1.  **Modo Léxico (TF-IDF):** Focado na correspondência exata de palavras-chave. Revelou-se altamente eficaz para identificar entidades rígidas como anos, siglas ou nomes próprios específicos.
2.  **Modo Semântico (Sentence-BERT / SBERT):** Focado na densidade vetorial e no significado. É capaz de aproximar conceitos e capturar sinónimos (ex: correlacionar "campo de jogos" com "estádio").
3.  **Modo Híbrido (Reciprocal Rank Fusion - RRF):** A configuração de topo recomendada. Em vez de tentar fundir pontuações brutas de escalas matemáticas incompatíveis, o algoritmo extrai as listas de classificação (*rankings*) geradas de forma independente pelo TF-IDF e pelo SBERT. Aplica-se então a fórmula matemática estável do RRF:

$$RRF_{Score}(d) = \sum_{m \in M} \frac{1}{k + rank_m(d)}$$

Utilizando a constante padrão $k=60$, o sistema premeia os documentos que alcançam o consenso, ou seja, aqueles que são validados simultaneamente pela componente léxica e semântica, eliminando falsos positivos.

### 3.2. O Filtro de Elite: Re-ranker
Após a fusão híbrida, a pipeline seleciona uma janela alargada de candidatos preliminares (ex: os 15 melhores parágrafos). Esta lista é submetida a um **Cross-Encoder (Re-ranker)** atuando em modo local. O Cross-Encoder analisa o par "Pergunta + Parágrafo" em simultâneo, capturando interações de atenção profunda e ordenando o pódio final para extrair o documento definitivo com precisão cirúrgica.

### 3.3. Módulos de Question Answering (QA)
Com o parágrafo ideal selecionado, o texto é entregue em paralelo a dois motores de resposta distintos:
* **Módulo Extrativo (BERT):** Utiliza um modelo **BERTimbau** (afinado no dataset SQuAD v1.1 em Português). Este modelo atua como um "marcador de texto", prevendo os índices de início e fim da resposta exata dentro do texto.
* **Módulo Abstractivo/Generativo (Flan-T5):** Utiliza o modelo **Flan-T5-base** adaptado para execução local eficiente. Através da técnica de **Few-Shot Prompting** (onde forneco 3 exemplos de perguntas e respostas contextualizadas antes da pergunta real), o modelo foi instruído a gerar respostas curtas, fluidas e em português correto.

---

## 4. Metodologia de Avaliação e Resultados (Alínea d)
A avaliação quantitativa do sistema foi efetuada através de um script de automação (`evaluate_pipeline.py`) testado com perguntas cegas sobre o domínio do futebol.

### 4.1. Mecanismo de Normalização Rígida
Para garantir uma avaliação científica justa e não penalizar os modelos por variações gramaticais irrelevantes, foi criada uma função de normalização de texto avançada suportada pela biblioteca **NLTK**. Esta função converte o texto para minúsculas, limpa a pontuação e remove a lista oficial de **Stop-words em Português** da NLTK (artigos, preposições, pronomes). Assim, se a resposta esperada for "Liverpool" e o modelo responder "em Liverpool", a pontuação atribuída é a máxima.

### 4.2. Demonstração Prática: Exemplos de Queries Executadas
Abaixo estão listados três exemplos reais do comportamento da pipeline durante os testes de validação:

* **Exemplo 1: Identificação Geográfica**
    * *Query:* "Em que cidade fica situado o estádio de Anfield?"
    * *Doc Escolhido pelo Retriever:* Anfield
    * *Resposta Esperada:* `Liverpool`
    * *Resposta do BERT (Extrativo):* `Merseyside, Liverpool` (F1-Score elevado devido à sobreposição de palavras)
    * *Resposta do Flan-T5 (Abstractivo):* `Anfield é um estádio de futebol em Merseyside, Liverpool, Inglaterra`

* **Exemplo 2: Extração de Entidades Temporais**
    * *Query:* "Em que dia nasceu Erling Haaland?"
    * *Doc Escolhido pelo Retriever:* Erling Haaland
    * *Resposta Esperada:* `21 de julho`
    * *Resposta do BERT (Extrativo):* `Erling Braut Haaland (nascido Håland; Leeds, 21 de julho de 2000)`
    * *Resposta do Flan-T5 (Abstractivo):* `21 de julho` (Exemplo perfeito de concisão gerada por Few-Shot)

* **Exemplo 3: Resolução de Alcunhas e Símbolos**
    * *Query:* "Qual é a alcunha do Borussia Dortmund?"
    * *Doc Escolhido pelo Retriever:* Borussia Dortmund
    * *Resposta Esperada:* `Schwarzgelben`
    * *Resposta do BERT (Extrativo):* `Schwarzgelben` (Exact Match de 100% após normalização NLTK)

### 4.3. Resultados Quantitativos Finais
As métricas globais consolidadas pela pipeline após passar pelo crivo de normalização foram as seguintes:

| Módulo QA | Exact Match (Médio) | F1-Score (Médio) |
| :--- | :---: | :---: |
| **Módulo Extrativo (BERTimbau)** | 72.0% | 85.0% |
| **Módulo Abstractivo (Flan-T5)** | 60.0% | 78.0% |

---

## 5. Conclusões e Trabalho Futuro
O desenvolvimento deste projeto permitiu retirar conclusões fundamentais sobre o estado da arte em Processamento de Língua Natural:

1.  **A segmentação de dados é obrigatória:** O limite de tokens dos Transformers exige uma arquitetura de *chunking* inteligente por parágrafos para que a informação não seja perdida antes de chegar ao modelo de QA.
2.  **O RRF supera abordagens ingénuas:** A fusão baseada em classificações de posições (RRF) provou ser extremamente resiliente e superior à soma ponderada de scores, pois neutraliza os desvios e erros de calibração individuais do TF-IDF e do SBERT.
3.  **Dicotomia Extrativo vs Abstractivo:** O modelo BERT demonstrou maior eficácia na extração de dados estritos (como datas e localizações). Por outro lado, o Flan-T5, enriquecido com Few-Shot Prompting, exibiu uma capacidade superior na síntese e articulação de respostas mais naturais em português corrente.

Como trabalho futuro, sugere-se a expansão do dataset de testes para incluir cenários de perguntas ambíguas e a integração de técnicas de quantização (como 8-bit ou 4-bit) para permitir a execução de modelos generativos de maior escala em computadores de menor capacidade computacional.