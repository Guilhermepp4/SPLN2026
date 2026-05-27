"""
evaluate_pipeline.py
--------------------
Avaliação quantitativa da PIPELINE COMPLETA (Alínea d).
Testa o fluxo: Pergunta -> Retriever (RRF) -> QA Módulos (BERT e Flan-T5).
"""

import json
import re
import nltk
from nltk.corpus import stopwords
from collections import Counter
from retriever import Retriever
from extrativa import ExtractiveQA
from abstrativa import AbstractiveQA

PT_STOPWORDS = set(stopwords.words('portuguese'))

EVAL_SET = [
    {"question": "Em que cidade fica situado o estádio de Anfield?", "expected": "Liverpool"},
    {"question": "Qual é a alcunha do Borussia Dortmund?", "expected": "Schwarzgelben"},
    {"question": "Em que dia nasceu Erling Haaland?", "expected": "21 de julho"},
    {"question": "Qual é o maior Clube de Portugal", "expected": "Benfica"},
    {"question": "Que oficial de vídeo é utilizado em competições de futebol?", "expected": "árbitro assistente de vídeo"}
]

def normalize_text(text: str) -> str:
    """Limpa pontuação, artigos e espaços para uma avaliação justa."""
    text = text.lower()    
    text = re.sub(r'[.\-–,!?();:]', ' ', text)
    words = text.split()
    filtered_words = [w for w in words if w not in PT_STOPWORDS]
    
    return " ".join(filtered_words)

def exact_match(prediction: str, ground_truth: str) -> int:
    """Devolve 1 se a resposta for exatamente igual à esperada, ou 0 se não."""
    return int(normalize_text(prediction) == normalize_text(ground_truth))

def f1_score(prediction: str, ground_truth: str) -> float:
    """Calcula a sobreposição de palavras entre a resposta dada e a esperada."""
    pred_tokens = normalize_text(prediction).split()
    truth_tokens = normalize_text(ground_truth).split()
    
    if len(pred_tokens) == 0 or len(truth_tokens) == 0:
        return float(pred_tokens == truth_tokens)
        
    common_tokens = Counter(pred_tokens) & Counter(truth_tokens)
    num_same = sum(common_tokens.values())
    
    if num_same == 0:
        return 0.0
        
    precision = 1.0 * num_same / len(pred_tokens)
    recall = 1.0 * num_same / len(truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1

def evaluate_pipeline():
    print("🤖 Inicializando a tua Pipeline de Futebol...")
    
    retriever = Retriever()
    extractive = ExtractiveQA()
    abstractive = AbstractiveQA()

    ext_em_scores = []
    ext_f1_scores = []
    abs_f1_scores = []

    print(f"\n🔍 A testar a pipeline completa com {len(EVAL_SET)} perguntas...")
    print("=" * 75)

    for i, example in enumerate(EVAL_SET, 1):
        question = example["question"]
        expected = example["expected"]

        print(f"\n[{i}] Pergunta: {question}")

        # --- PASSO 1: O TEU RETRIEVER ENTRA EM ACÇÃO (RRF + Re-ranker) ---
        hits = retriever.search(question, mode="hybrid", top_k=1, use_reranker=True)
        
        if not hits:
            print("    ⚠️ O Retriever não encontrou nenhum parágrafo relevante.")
            continue
            
        best_doc = hits[0][0]
        context_retrieved = best_doc["text"]
        print(f"    Doc Escolhido: {best_doc['title']}")

        # --- PASSO 2: OS MODELOS DE QA ENTRAN EM ACÇÃO ---
        # QA Extrativo (O teu BERT do Colab)
        ext_answer = extractive.predict(question, context_retrieved)
        em = exact_match(ext_answer, expected)
        f1_ext = f1_score(ext_answer, expected)
        ext_em_scores.append(em)
        ext_f1_scores.append(f1_ext)

        # QA Abstractivo (O teu Flan-T5 com Few-Shot)
        abs_answer = abstractive.predict(question, context_retrieved)
        f1_abs = f1_score(abs_answer, expected)
        abs_f1_scores.append(f1_abs)

        print(f"    Esperado    : {expected}")
        print(f"    👉 Extrativo  : {ext_answer} (F1: {f1_ext:.2f})")
        print(f"    👉 Abstractivo: {abs_answer} (F1: {f1_abs:.2f})")

    # --- RESULTADOS GLOBAIS DA TUA PIPELINE ---
    n = len(EVAL_SET)
    print("\n" + "=" * 75)
    print("📊 RELATÓRIO FINAL DA TUA PIPELINE (Alínea d)")
    print("=" * 75)
    print(f"Módulo Extrativo (O teu BERT do Colab):")
    print(f"  Exact Match médio : {(sum(ext_em_scores)/n)*100:.1f}%")
    print(f"  F1-Score médio    : {(sum(ext_f1_scores)/n)*100:.1f}%")
    print("-" * 75)
    print(f"Módulo Abstractivo (Flan-T5 com Few-Shot):")
    print(f"  F1-Score médio    : {(sum(abs_f1_scores)/n)*100:.1f}%")
    print("=" * 75)

if __name__ == "__main__":
    evaluate_pipeline()