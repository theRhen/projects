from func_maquininha import maquininha

loja = input("Loja: ").upper() # loja(variable) recebe entrada.maiúsculo
descricao = input("Descrição: ").lower() # descricao(variable) recebe entrada.minúsculo
valor_str = maquininha()  # valor_str(variable) recebe maquininha(função)
data = input("\nData: ") # data(variable) recebe entrada

print("-----------------------------------")
print("|           NOTA FISCAL           |")
print("-----------------------------------")
print(f"Loja: *{loja}*")
print(f"Descrição: {descricao}")
print(f"Valor: {valor_str}")
print(f"Data: {data}")
print("-----------------------------------")
print("|  compra cadastrada com sucesso  |")
print("-----------------------------------")

# Pausa final para o programa não fechar automaticamente
input("\nPressione ENTER para sair...")
