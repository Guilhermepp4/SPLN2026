import json
import pickle
import os
import numpy as np
from typing import Literal

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, CrossEncoder, util
import torch

# ---------------------------------------------------------------------------
# Configurações Avançadas e Modelos de Referência
# ---------------------------------------------------------------------------
SBERT_MODEL         = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
CROSS_ENCODER_MODEL = "BAAI/bge-reranker-base"
CACHE_TFIDF         = "cache_tfidf.pkl"
CACHE_SBERT         = "cache_sbert.pt"
RERANK_CANDIDATES   = 15    
RERANK_CONTEXT_LEN  = 512   

class Retriever:
    """
    Retriever Avançado com Fusão por Posto Recíproco (RRF) e Re-ranking Semântico.
    Desenvolvido especificamente para análises factuais do corpus de futebol.
    """

    def __init__(
        self,
        corpus_path: str = "docs/corpus_futebol_limpo.json",
        sbert_model: str = SBERT_MODEL,
        use_cache: bool = True,
    ):
        print("⚙️ Inicializando Arquitetura Exclusiva do Retriever...")
        if not os.path.exists(corpus_path):
            raise FileNotFoundError(f"Erro: O ficheiro '{corpus_path}' não foi encontrado.")

        with open(corpus_path, "r", encoding="utf-8") as f:
            corpus_original = json.load(f)

        self.corpus = []
        for doc in corpus_original:
            for p in doc["text"]:
                self.corpus.append({
                    "id_original": doc["id"],
                    "title": doc["title"],
                    "text": p,
                    "url": doc["url"]
                })

        self.texts     = [doc["text"] for doc in self.corpus]
        self.use_cache = use_cache
        self.cross_encoder = None   

        # DOCKING DE STOP-WORDS: Expandido com termos redundantes do domínio do futebol
        self.pt_stop_words = [
            'o', 'a', 'os', 'as', 'de', 'do', 'da', 'dos', 'das', 'em', 'no', 'na', 
            'nos', 'nas', 'e', 'que', 'um', 'uma', 'uns', 'umas', 'com', 'por', 'para',
            'ao', 'à', 'aos', 'às', 'se', 'mais', 'como', 'foi', 'foram', 'clube', 
            'futebol', 'jogadores', 'equipa', 'partida', 'jogo', 'campeonato'
        ]

        self._build_tfidf_index()
        self._build_sbert_index(sbert_model)
        print("🚀 Sistema RRF pronto e operacional!\n")

    def _build_tfidf_index(self) -> None:
        if self.use_cache and os.path.exists(CACHE_TFIDF):
            print("  [Índice Léxico] A carregar cache estruturado...")
            with open(CACHE_TFIDF, "rb") as f:
                data = pickle.load(f)
            self.tfidf_vectorizer = data["vectorizer"]
            self.tfidf_matrix     = data["matrix"]
        else:
            print("  [Índice Léxico] A criar representação esparsa (TF-IDF)...")
            self.tfidf_vectorizer = TfidfVectorizer(
                stop_words=self.pt_stop_words,
                ngram_range=(1, 3), # Expandido para capturar trigramas (ex: "Sporting Clube Portugal")
                max_df=0.80,
                min_df=1,
                sublinear_tf=True,
            )
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.texts)
            if self.use_cache:
                with open(CACHE_TFIDF, "wb") as f:
                    pickle.dump({"vectorizer": self.tfidf_vectorizer, "matrix": self.tfidf_matrix}, f)

    def _build_sbert_index(self, model_name: str) -> None:
        if self.use_cache and os.path.exists(CACHE_SBERT):
            print("  [Índice Semântico] A carregar embeddings vetoriais...")
            self.sbert_embeddings = torch.load(CACHE_SBERT)
        else:
            print(f"  [Índice Semântico] A instanciar codificador multilingue...")
            self.sbert_model = SentenceTransformer(model_name)
            self.sbert_embeddings = self.sbert_model.encode(
                self.texts,
                convert_to_tensor=True,
                show_progress_bar=True,
                batch_size=32,
            )
            if self.use_cache:
                torch.save(self.sbert_embeddings, CACHE_SBERT)

        if not hasattr(self, "sbert_model"):
            self.sbert_model = SentenceTransformer(model_name)

    def _rerank(self, query: str, candidates: list, top_k: int) -> list:
        if self.cross_encoder is None:
            self.cross_encoder = CrossEncoder(CROSS_ENCODER_MODEL)

        pairs = [(query, doc["text"][:RERANK_CONTEXT_LEN]) for doc, _ in candidates]
        cross_scores = self.cross_encoder.predict(pairs)

        reranked = sorted(
            zip([doc for doc, _ in candidates], cross_scores),
            key=lambda x: x[1],
            reverse=True,
        )
        return [(doc, float(score)) for doc, score in reranked[:top_k]]

    # ── Métodos de Pesquisa Core ──────────────────────────────────────────────

    def _get_ranked_indices(self, scores: np.ndarray) -> list:
        """Devolve os índices ordenados do melhor para o pior score."""
        return np.argsort(scores)[::-1].tolist()

    def search(
        self,
        query: str,
        mode: Literal["lexical", "semantic", "hybrid"] = "hybrid",
        top_k: int = 2,
        k_rrf: int = 60,  # Parâmetro de suavização padrão do algoritmo RRF
        use_reranker: bool = False,
    ) -> list:
        
        # 1. Pesquisa Léxica (TF-IDF)
        q_vec = self.tfidf_vectorizer.transform([query])
        lex_scores = cosine_similarity(q_vec, self.tfidf_matrix).flatten()
        
        # 2. Pesquisa Semântica (SBERT)
        q_emb = self.sbert_model.encode(query, convert_to_tensor=True)
        sem_scores = util.pytorch_cos_sim(q_emb, self.sbert_embeddings).cpu().numpy().flatten()

        if mode == "lexical":
            top_indices = self._get_ranked_indices(lex_scores)[:top_k]
            return [(self.corpus[i], float(lex_scores[i])) for i in top_indices]

        elif mode == "semantic":
            top_indices = self._get_ranked_indices(sem_scores)[:top_k]
            return [(self.corpus[i], float(sem_scores[i])) for i in top_indices]

        elif mode == "hybrid":
            # ── NOVO MOTOR DE PENSAMENTO: RECIPROCAL RANK FUSION (RRF) ──
            # Em vez de misturar notas, avaliamos o consenso de posição dos rankings.
            rrf_scores = np.zeros(len(self.corpus))
            
            lex_rank = self._get_ranked_indices(lex_scores)
            sem_rank = self._get_ranked_indices(sem_scores)

            # Aplica a fórmula matemática estável do RRF
            for rank_pos, doc_idx in enumerate(lex_rank):
                rrf_scores[doc_idx] += 1.0 / (k_rrf + (rank_pos + 1))
                
            for rank_pos, doc_idx in enumerate(sem_rank):
                rrf_scores[doc_idx] += 1.0 / (k_rrf + (rank_pos + 1))

            # Determina o número de alvos a extrair
            n_candidates = RERANK_CANDIDATES if use_reranker else top_k
            top_indices = np.argsort(rrf_scores)[::-1][:n_candidates]
            candidates = [(self.corpus[i], float(rrf_scores[i])) for i in top_indices]

            if use_reranker:
                candidates = self._rerank(query, candidates, top_k)

            return candidates
        else:
            raise ValueError(f"Modo desconhecido: '{mode}'")

# ---------------------------------------------------------------------------
# Visualização Gráfica dos Resultados
# ---------------------------------------------------------------------------
def print_results(results: list, query: str, mode: str) -> None:
    print(f"\n⚡ [RRF ENGINE] Pergunta: \"{query}\"")
    print(f"   Estratégia Aplicada: {mode.upper()}")
    print(f"   Top {len(results)} Passagens Selecionadas:")
    print("   " + "─" * 70)
    for i, (doc, score) in enumerate(results, 1):
        print(f"   [{i}] Score Confiança: {score:.5f} | Artigo: {doc['title']}")
        print(f"       📝 Excerpt: {doc['text'][:140]}...\n")
    print("   " + "═" * 70)

if __name__ == "__main__":
    r = Retriever()
    pergunta = "Em que ano foi fundado o Barcelona e quem foi o seu fundador?"
    
    res = r.search(pergunta, mode="hybrid", top_k=2, use_reranker=True)
    print_results(res, pergunta, "hybrid + cross-encoder rerank")