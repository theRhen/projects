from func_maquininha import maquininha
from datetime import datetime

# Lista que armazenará todas as notas (em memória)
notas = []

while True:
    loja = input("Loja: ").upper()
    descricao = input("Descrição: ").strip().title()
    valor_str = maquininha()

    # Validação da data
    while True:
        data_input = input("\nData (DD/MM/AAAA): ").strip()
        try:
            data = datetime.strptime(data_input, "%d/%m/%Y").date()
            break
        except ValueError:
            print("⚠️ Data inválida! Digite no formato DD/MM/AAAA.") 

    # Cria um dicionário para a nota
    nota = {
        "loja": loja,
        "descricao": descricao,
        "valor": valor_str,
        "data": data.strftime('%d/%m/%Y')
    }

    # Adiciona na lista
    notas.append(nota)

    # Salva no arquivo .txt (append, para não apagar as anteriores)
    with open("notas.txt", "a", encoding="utf-8") as f:
        f.write("-----------------------------------\n")
        f.write("|           NOTA FISCAL           |\n")
        f.write("-----------------------------------\n")
        f.write(f"Loja: {nota['loja']}\n")
        f.write(f"Descrição: {nota['descricao']}\n")
        f.write(f"Valor: {nota['valor']}\n")
        f.write(f"Data: {nota['data']}\n")
        f.write("-----------------------------------\n")
        f.write("|  compra cadastrada com sucesso  |\n")
        f.write("-----------------------------------\n\n")

    print("\nNota fiscal salva em notas.txt ✅")

    # Pergunta se deseja cadastrar outra
    continuar = input("Deseja cadastrar outra nota? (s/n): ").lower()
    if continuar != "s":
        break

input("\nPressione ENTER para sair...")
