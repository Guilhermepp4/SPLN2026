# Atlas da Saúde - Web Scraper de Doenças

Este projeto consiste num **script em Python** que faz web scraping ao site **Atlas da Saúde** para recolher informação sobre doenças de **A a Z**.

O script percorre todas as páginas de doenças organizadas por letra, extrai várias informações relevantes e guarda os dados num ficheiro **JSON estruturado**.

## 📊 Dados extraídos

Para cada doença, o script recolhe:

* **Descrição Pequena** – pequeno resumo da doença
* **Descrição Grande** – descrição completa
* **Causas**
* **Sintomas**
* **Tratamento**
* **Artigos Relacionados**

Os dados são guardados no ficheiro:

```
doencas.json
```

com a seguinte estrutura:

```json
{
  "Nome da Doença": {
    "Descricão Pequena": "...",
    "Descricão Grande": "...",
    "Causas": "...",
    "Sintomas": ["..."],
    "Tratamento": "...",
    "Artigos Relacionados": []
  }
}
```
## 📦 Instalação

1. Clonar o repositório

```bash
git clone https://github.com/teu-username/nome-do-repositorio.git
cd nome-do-repositorio
```

2. Instalar dependências

```bash
pip install requests beautifulsoup4
```

## ▶️ Como executar

Executa o script com:

```bash
python scraping.py
```

O programa irá:

1. Percorrer todas as letras de **A a Z**
2. Aceder às páginas de doenças do site
3. Extrair as informações detalhadas
4. Guardar tudo no ficheiro **doencas.json**

## 🔎 Funcionamento do script

O script funciona em duas etapas principais:

### 1. Recolha das páginas por letra

O programa percorre todas as letras do alfabeto:

```
https://www.atlasdasaude.pt/doencasaaz/a
https://www.atlasdasaude.pt/doencasaaz/b
...
https://www.atlasdasaude.pt/doencasaaz/z
```

### 2. Extração da informação

Para cada doença encontrada:

* entra na página individual da doença
* analisa o HTML com **BeautifulSoup**
* identifica secções como:

```
Descrição
Causas
Sintomas
Tratamento
```

* guarda os dados numa estrutura Python
* exporta para **JSON**

## ⚠️ Aviso

Este projeto foi desenvolvido para **fins educativos** e demonstração de técnicas de **web scraping**.

O conteúdo pertence ao site original:
https://www.atlasdasaude.pt