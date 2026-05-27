"""
qa_abstractive.py
-----------------
Módulo de QA Abstractivo usando Flan-T5-large via prompting.

Ao contrário do QA extrativo (BERT), este módulo gera a resposta
em linguagem natural -- não se limita a extrair um pedaço (span) do texto.
Usa as instruções (prompt) para responder em português.

Uso:
    python qa_abstractive.py
"""

import torch
from transformers import T5ForConditionalGeneration, AutoTokenizer

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------
MODEL_NAME  = "google/flan-t5-base"
MAX_INPUT   = 512
MAX_OUTPUT  = 128
INTRO_WORDS = 350   # Número de palavras iniciais do artigo a usar como contexto


# ---------------------------------------------------------------------------
# Classe Principal
# ---------------------------------------------------------------------------
class AbstractiveQA:
    """
    QA Abstractivo via prompting ao Flan-T5-large.
    
    Usa as primeiras INTRO_WORDS palavras do documento mais relevante
    como contexto para responder à pergunta em português.
    """

    def __init__(self, model_name: str = MODEL_NAME):
        print(f"🔄 A carregar modelo generativo '{model_name}'...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model     = T5ForConditionalGeneration.from_pretrained(model_name)
        
        # Define o dispositivo (usa GPU se disponível, caso contrário CPU)
        self.device    = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()
        print(f"🚀 Modelo pronto no dispositivo: {self.device}\n")

    def predict(self, question: str, context: str) -> str:
        """
        Gera uma resposta em linguagem natural usando Few-Shot Prompting em PT.
        """
        if isinstance(context, list):
            context = " ".join(context)

        words   = context.split()
        excerpt = " ".join(words[:INTRO_WORDS])

        # FEW-SHOT PROMPTING: Ensinamos o modelo com exemplos antes da pergunta real
        prompt = (
            f"Instrução: Atuando como um especialista em futebol, lê o contexto e responde à pergunta em Português de forma curta.\n\n"
            f"Exemplo 1:\n"
            f"Contexto: O Sporting Clube de Portugal foi fundado a 1 de julho de 1906 por iniciativa de José Alvalade.\n"
            f"Pergunta: Quem fundou o Sporting?\n"
            f"Resposta: José Alvalade.\n\n"
            f"Exemplo 2:\n"
            f"Contexto: O Real Madrid conquistou a sua décima Liga dos Campeões no ano de 2014 em Lisboa.\n"
            f"Pergunta: Em que ano o Real Madrid ganhou a décima?\n"
            f"Resposta: 2014.\n\n"
            f"Agora é a tua vez:\n"
            f"Contexto: {excerpt}\n"
            f"Pergunta: {question}\n"
            f"Resposta:"
        )

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            max_length=MAX_INPUT,
            truncation=True,
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=MAX_OUTPUT,
                num_beams=4,
                early_stopping=True,
                no_repeat_ngram_size=2,
            )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()


# ---------------------------------------------------------------------------
# Bloco de Teste Local
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Teste rápido e isolado para ver o Flan-T5 a funcionar em português
    qa = AbstractiveQA()
    
    contexto_exemplo = (
        "O Sport Lisboa e Benfica foi fundado no dia 28 de fevereiro de 1904. "
        "O clube joga os seus jogos caseiros no Estádio da Luz, localizado em Lisboa, "
        "que tem uma capacidade para mais de 65 mil espetadores."
    )
    pergunta_exemplo = "Qual é o estádio onde o Benfica joga?"
    
    resposta = qa.predict(pergunta_exemplo, contexto_exemplo)
    print("-" * 50)
    print(f"Pergunta: {pergunta_exemplo}")
    print(f"👉 Resposta Gerada: {resposta}")
    print("-" * 50)