from func_maquininha import maquininha
from datetime import datetime

loja = input("Loja: ").upper() # loja(variable) recebe entrada.maiúsculo
descricao = input("Descrição: ").strip().title() # descricao(variable) recebe entrada.minúsculo
valor_str = maquininha()  # valor_str(variable) recebe maquininha(função)
while True: # laço while para validar a data (só sai quando for digitada corretamente)
    data_input = input("\nData (DD/MM/AAAA): ").strip()
    try:
        data = datetime.strptime(data_input, "%d/%m/%Y").date()
        break
    except ValueError:
        print("⚠️ Data inválida! Digite no formato DD/MM/AAAA.") 

print("-----------------------------------")
print("|           NOTA FISCAL           |")
print("-----------------------------------")
print(f"Loja: *{loja}*")
print(f"Descrição: {descricao}")
print(f"Valor: {valor_str}")
print(f"Data: {data.strftime('%d/%m/%Y')}")
print("-----------------------------------")
print("|  compra cadastrada com sucesso  |")
print("-----------------------------------")

# Pausa final para o programa não fechar automaticamente
input("\nPressione ENTER para sair...")
