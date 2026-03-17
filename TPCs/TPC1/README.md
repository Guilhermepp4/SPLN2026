# Extração de Conceitos Médicos – SPLN2026

Este projeto tem como objetivo **extrair conceitos de um XML médico (`medicina.xml`)** e convertê-los num ficheiro JSON estruturado, mantendo campos opcionais, traduções e metadados.

---

## 1. Objetivo

O script processa o XML e gera um ficheiro JSON (`dicionario_mediciona.json`) com a seguinte estrutura:

- `id`: número único do conceito.
- `ga`: nome do conceito em galego.
- `dom`: domínios do conceito (opcional).
- `sin`: sinónimos (opcional).
- `var`: variantes (opcional).
- `nota`: notas associadas (opcional).
- Traduções por língua (`pt`, `es`, `en`, `la`) extraídas do conteúdo `<i>` (opcional).

Exemplo simplificado:

```json
{
    "1": {
        "ga": "abdome agudo",
        "dom": "Anatomia",
        "sin": "abdômen agudo",
        "var": null,
        "nota": null,
        "pt": "abdômen agudo",
        "es": "abdomen agudo",
        "en": "acute abdomen",
        "la": null
    }
}
```

## 2. Estrutura do Código
### 2.1 Leitura e Pré-processamento
Substitui `\d+` por `@@\d+` para marcar claramente o início de cada conceito.
`re.split` divide o conteúdo do XML em substrings individuais para processamento por conceito.

## 2.2 Função `processar_conceito`
Esta função recebe cada substring (conceito) e extrai os campos:
O regex `blocos` captura cada tradução por língua, mesmo que haja múltiplas linhas.
As expressões regulares para `sin`, `var` e `nota` utilizam os marcadores `@` adicionados no pré-processamento.
Todos os campos são adicionados ao dicionário final do conceito.

## 2.3 Processamento de Todos os Conceitos
Começa do índice 1 porque o primeiro elemento do `split` antes do primeiro `@@` é vazio.
O resultado é um dicionário com todos os conceitos, indexado pelo `id`.

# 3. Observações
O código foi projetado para lidar com estruturas variantes do XML, incluindo IDs isolados, campos juntos ou separados e múltiplas traduções.
Todos os campos opcionais são tratados como None se não forem encontrados.
Expressões regulares e marcadores @ permitem extrair dados de forma consistente e segura.
O JSON final pode ser usado para análises futuras ou integração em aplicações.

# Executar o script principal
python3 extractConcepts.py

# Resultado
Um ficheiro JSON chamado dicionario_mediciona.json com todos os conceitos