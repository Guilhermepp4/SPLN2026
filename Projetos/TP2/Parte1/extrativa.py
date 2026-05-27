"""
qa_extractive.py
----------------
Módulo de QA Extrativo baseado em BERT.
Carrega o modelo que treinaste no Google Colab para extrair
a resposta exata a partir do contexto fornecido pelo Retriever.
"""

import os
import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

# Caminho para a pasta onde guardaste o teu modelo do Colab
MODEL_PATH = "models/bert-squad-portuguese"

MAX_LENGTH = 384
DOC_STRIDE = 128

class ExtractiveQA:
    """
    Classe responsável por carregar o teu modelo BERT treinado
    e extrair a resposta exata de dentro de um texto em português.
    """
    def __init__(self, model_path: str = MODEL_PATH):
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"\n[ERRO] Não encontrei a pasta do teu modelo em '{model_path}'.\n"
            )

        print(f"🔄 A carregar o modelo de QA Extrativo local ({model_path})...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForQuestionAnswering.from_pretrained(model_path)
        
        # Define o dispositivo (usa GPU se o teu PC tiver, caso contrário usa CPU)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()
        print(f"🚀 Modelo carregado com sucesso no dispositivo: {self.device}\n")

    def predict(self, question: str, context: str) -> str:
        """
        Dada uma pergunta e um contexto (parágrafo), extrai o pedaço de texto
        onde se encontra a resposta exata.
        """
        inputs = self.tokenizer(
            question,
            context,
            max_length=MAX_LENGTH,
            truncation="only_second",
            stride=DOC_STRIDE,
            return_tensors="pt",
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)

        # Escolhe os tokens com maior probabilidade de início e fim da resposta
        start_scores = outputs.start_logits
        end_scores = outputs.end_logits

        answer_start = torch.argmax(start_scores)
        answer_end = torch.argmax(end_scores) + 1

        # Converte os tokens de volta para texto normal
        answer = self.tokenizer.convert_tokens_to_string(
            self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end])
        )
        
        # Limpa caracteres especiais de formatação do BERT
        answer = answer.replace("[CLS]", "").replace("[SEP]", "").strip()
        
        if not answer or answer == "":
            return "Não foi possível extrair uma resposta do texto."
            
        return answer


# ---------------------------------------------------------------------------
# Bloco de Teste Local (Apenas corre se executares este ficheiro diretamente)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        # Instancia a classe que criámos acima
        qa = ExtractiveQA()
        
        # Texto e pergunta de teste
        contexto_exemplo = (
            "O Cristiano Ronaldo nasceu no Funchal, na Madeira, a 5 de fevereiro de 1985. "
            "Começou a sua carreira sénior no Sporting CP antes de se mudar para o Manchester United em 2003."
        )
        pergunta_exemplo = "Em que ano o Cristiano Ronaldo foi para o Manchester United?"
        
        # Pede ao teu modelo para responder
        resposta = qa.predict(pergunta_exemplo, contexto_exemplo)
        print("-" * 60)
        print(f"Pergunta: {pergunta_exemplo}")
        print(f"👉 Resposta Extraída pelo teu BERT: {resposta}")
        print("-" * 60)
        
    except FileNotFoundError as e:
        print(e)