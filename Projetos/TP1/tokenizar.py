import nltk
import math
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import ngrams
from collections import defaultdict
from info import FILES,openFileRead
import json

def tokenize(text):
    """Tokeniza o texto em palavras usando nltk."""
    tokens = word_tokenize(text)
    tokens = [t.lower() for t in tokens if t.isalpha()]
    return tokens

def build_ngram_model(tokens, n=3):
    """
    Constrói um modelo de n-gramas com probabilidades de transição.
    Igual ao padrão do exerciciodaaula.py.
    """
    n_grams = list(ngrams(tokens, n))
    model = defaultdict(lambda: defaultdict(lambda: 0))

    for gram in n_grams:
        prefix = tuple(gram[:-1])
        next_word = gram[-1]
        model[prefix][next_word] += 1

    for prefix in model:
        total_count = float(sum(model[prefix].values()))
        for next_word in model[prefix]:
            model[prefix][next_word] /= total_count

    return model

def score_sentence(model, sentence_tokens, vocab_size, n=3):
    
    if len(sentence_tokens) < n:
        return float('-inf')

    score = 0.0
    count = 0

    for gram in ngrams(sentence_tokens, n):
        prefix = tuple(gram[:-1])
        next_word = gram[-1]
        
        prefix_counts = model.get(prefix, {})
        numerator = prefix_counts.get(next_word, 0) + 1          
        denominator = sum(prefix_counts.values()) + vocab_size
        
        prob = numerator / denominator
        score += math.log(prob)
        count += 1

    return score / count

def top3Func(scored_sentences):
    scoredOrder = sorted(scored_sentences, key=lambda x: x[1], reverse=True)
    top3 = []
    for sentence, score in scoredOrder:
        if len(top3) > 3:
            break

        sentenceT = set(tokenize(sentence))
        similar = False
        for sent, _ in top3:
            sentT = set(tokenize(sent))
            diff = len(sentT & sentenceT) / max(len(sentT | sentenceT), 1)
            
            if diff > 0.50:
                similar = True
                break
        if not similar:
            top3.append((sentence, score))

    top3Order = sorted(top3, key=lambda x: x[1], reverse = True)[:3]
    return top3Order


def main():
    topSentences = {}
    allTokens = []
    filesTokens = {}

    for key, file in FILES.items():
        text = openFileRead(file['idCleaned'])
        fileTokens = tokenize(text)
        filesTokens[key] = fileTokens
        allTokens.extend(fileTokens)
        print(f"\n{key}:")
        print(f"  Tokens totais:  {len(fileTokens)}")
        print(f"  Vocab único:    {len(set(fileTokens))}")
        print(f"  Primeiros 10:   {fileTokens[:10]}")

    print(f"\nCorpus completo: {len(allTokens)} tokens | {len(set(allTokens))} únicos")

    N = input("Quantos n-grams pertende? ")
    model = build_ngram_model(allTokens, n=int(N))
    print(f"Contextos únicos: {len(model)}")
    
    tamanho = len(allTokens)
    for key, file in FILES.items():
        scored_sentences = []
        text = openFileRead(file['idCleaned'])
        sentences = sent_tokenize(text)
        for sentence in sentences: 
            tokens_sentence = tokenize(sentence)
            score = score_sentence(model, tokens_sentence, tamanho, n=int(N))
            scored_sentences.append((sentence, score))
        
        top3 = top3Func(scored_sentences)

        topSentences.setdefault(key, {})
        for s, sc in top3:
            topSentences[key][s] = sc
            print(f"Sentence: {s} -> {sc} score\n")
        
    f_out = open("infoFiles/top3Frases.json", "w")
    json.dump(topSentences, f_out, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()