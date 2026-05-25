import json
import wikipediaapi

# 1. Configurar a API da Wikipédia (Língua: Português)
# O user_agent é obrigatório para a Wikipédia saber quem está a aceder
wiki = wikipediaapi.Wikipedia(
    user_agent='MeuProjetoEscolarRAG/1.0 (meuemail@escola.com)',
    language='pt'
)

# 2. Lista de páginas da Wikipédia sobre futebol para recolher informação
paginas_futebol = [
    # --- Clubes de Portugal ---
    "Futbol Club Barcelona", "Real Madrid Club de Fútbol", "Sporting Clube de Portugal",
    "Sport Lisboa e Benfica", "Futebol Clube do Porto", "Vitória Sport Clube", 
    "Sporting Clube de Braga", "Boavista Futebol Clube", "Belenenses Futebol SAD", 
    "Rio Ave Futebol Clube", "Gil Vicente Futebol Clube", "Grupo Desportivo de Chaves",
    
    # --- Clubes Internacionais (Inglaterra, Itália, Espanha, etc.) ---
    "Manchester United Football Club", "Manchester City Football Club", "Liverpool Football Club", 
    "Arsenal Football Club", "Chelsea Football Club", "Tottenham Hotspur Football Club",
    "Juventus Football Club", "Associazione Calcio Milan", "Inter de Milão", "Feyenoord Rotterdam",
    "Associazione Sportiva Roma", "Società Sportiva Lazio", "Club Atlético de Madrid",
    "Paris Saint-Germain Football Club", "Fraserburgh Football Club", "FC Bayern München", 
    "Borussia Dortmund", "Ajax Amsterdão", "Boca Juniors", "Sport Club Corinthians Paulista", 
    "Clube de Regatas do Flamengo", "Sociedade Esportiva Palmeiras", "Santos Futebol Clube",

    # --- Jogadores Históricos e Atuais ---
    "Cristiano Ronaldo", "Lionel Messi", "Pelé", "Diego Maradona", "Eusébio", 
    "Johan Cruyff", "Zinedine Zidane", "Ronaldo Nazário", "Ronaldinho Gaúcho", 
    "Neymar", "Kylian Mbappé", "Erling Haaland", "Luka Modrić", "Karim Benzema", 
    "Luís Figo", "Rui Costa", "Deco", "Paulo Futre", "Alfredo Di Stéfano", "Di Maria",
    "Franz Beckenbauer", "Michel Platini", "Gerd Müller", "Zico", "Garrincha",

    # --- Treinadores Icónicos ---
    "José Mourinho", "Pep Guardiola", "Alex Ferguson", "Carlo Ancelotti", 
    "Jürgen Klopp", "Arsène Wenger", "Rúben Amorim", "Jorge Jesus", 
    "Sérgio Conceição", "Fernando Santos (treinador)", "Zinedine Zidane",

    # --- Competições e Organizações ---
    "Futebol", "História do futebol", "Regras do futebol", "Liga dos Campeões da UEFA", 
    "Copa do Mundo FIFA", "Seleção Portuguesa de Futebol", "Campeonato Português de Futebol", 
    "UEFA Europa League", "Campeonato Europeu de Futebol", "Copa América", 
    "Taça de Portugal", "Taça da Liga", "Premier League", "La Liga", "Serie A (Itália)", 
    "Bundesliga", "Federação Portuguesa de Futebol", "FIFA", "UEFA",

    # --- Estádios de Futebol ---
    "Estádio da Luz", "Estádio do Dragão", "Estádio José Alvalade", "Camp Nou", 
    "Estádio Santiago Bernabéu", "Estádio de Wembley", "Estádio do Maracanã", 
    "San Siro", "Old Trafford", "Anfield", "Allianz Arena", "Estádio da Capital do Móvel",

    # --- Prémios e Conceitos ---
    "Bola de Ouro", "The Best FIFA Football Awards", "Bota de Ouro da UEFA", 
    "Golo", "Guarda-redes", "Árbitro (futebol)", "Substituição (futebol)", 
    "Cartão amarelo", "Cartão vermelho", "Fora de jogo", "Penálti", 
    "Prolongamento", "Desempate por pontapés da marca de grande penalidade", 
    "Tiki-taka", "Janela de transferências"
]

corpus_final = []

print("A iniciar a recolha de documentos da Wikipédia...")

for titulo in paginas_futebol:
    page = wiki.page(titulo)
    counter = 1
    
    doc_corpus = []
    if page.exists():
        print(f"-> A processar: {page.title}")
        
        paragrafos = page.text.split('\n')
        
        for p in paragrafos:
            texto_limpo = p.strip()
            
            doc_corpus.append(texto_limpo)
    
    if len(doc_corpus) > 0:
        documento = {
            "title": f"{page.title}",
            "text": doc_corpus,
            "url": page.fullurl,
            "id": counter
        }
        corpus_final.append(documento)
            
        counter += 1

print(f"\nRecolha concluída! Total de documentos gerados: {len(corpus_final)}")

nome_ficheiro = "corpus_futebol.json"
with open(nome_ficheiro, "w", encoding="utf-8") as f:
    json.dump(corpus_final, f, ensure_ascii=False, indent=2)

print(f"Sucesso! O teu corpus foi guardado em '{nome_ficheiro}' pronto para o projeto.")