import subprocess

SCRIPTS = [
    (1, "extract.py", "Extração e limpeza de texto"),
    (2, "tokenizar.py", "Transformar em tokens o texto e obter o top3 frases"),
    (3, "NER.py", "Executar o NER com Spacy"),
    (4, "generateLatex.py", "Gerar artigos Latex"),
]

def wait_for_key():
    """Espera que o usuário pressione qualquer tecla (precisa Enter)"""
    input("\nPressione qualquer tecla e Enter para continuar...")

def execScript(script):
    try:
        subprocess.run(["python3", script], check=True)
        print(f"✔ {script} concluído com sucesso!")
        return 0
    except subprocess.CalledProcessError:
        print(f"❌ Ocorreu um erro ao executar {script}")
        return -1
        
def main():
    """Bem-vindo a minha proposta de resolução do TP1 de SPLN"""
    print("\n" + "-"*60)
    print("-"*13+" Bem vindo a historia de Protugal "+ "-"*13)
    print("-"*60 + "\n")

    wait_for_key()
    for number, script, description in SCRIPTS:
        print(f"\n[{number}] Executando: {description} ({script})")
        stats = execScript(script)

        if stats == 0 and number != 4:
            wait_for_key()
        elif stats == -1:
            break


if __name__ == "__main__":
    main()
