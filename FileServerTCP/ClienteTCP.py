import socket
import os
import json

HOST = '192.168.56.1' # IP do cliente (IP do HOST cliente)
PORT = 20000          # Definindo a porta

# Criando o socket TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect((HOST, PORT)) # Ligando o socket a porta

# Entrada da operação
operacao = int(input("Digite a operação (10 = Download - 20 = Listagem): "))

# Datagrama Operação (Número da operação 1 BYTE)
operacao_to_bytes = operacao.to_bytes(1, "big") # BYTES (Bytes ⭠ Inreiro) (Número inteiro da operação ⭢ 1 Byte)
tcp_socket.sendall(operacao_to_bytes) # CLIENTE ENVIANDO Datagrama Operação
print(f"[OK] Operação {operacao} enviada\n")

# REQUISIÇÃO DE DOWNLOAD (Se Operacao == 10)
if operacao == 10:
    #Entrada da requisição
    nome_file = input("Nome do arquivo (ex: exemplo.txt): ")
    print()
    
    # Converte o nome do arquivo para bytes
    nome_bytes = nome_file.encode('utf-8') # BYTES (Bytes ⭠ String) (ex: exemplo.txt ⭢ b'exemplo.txt')
    # Calcula o tamanho do nome em bytes "Percorre cada caracter"
    tamanho_file = len(nome_bytes) # INTEIRO (Inteiro ⭠ Bytes) (ex: exemplo.txt ⭢ 11)

    # Datagrama 1 (Tamanho do nome do arquivo 1 BYTE)
    tamanho_to_bytes = tamanho_file.to_bytes(1, "big") # BYTES (1 Byte ⭠ Inteiro) (Tamanho do nome do arquivo ⭢ 1 Byte)
    tcp_socket.sendall(tamanho_to_bytes) # CLIENTE ENVIANDO Primeiro Datagrama
    print(f"[OK] Primeiro datagrama enviado: tamanho = {tamanho_file} byte(s)")

    # Datagrama 2 (Nome do arquivo VÁRIOS BYTES)
    nome_to_bytes = nome_bytes # BYTES (Bytes ⭠ Bytes) (Nome do arquivo ⭢ Nova variável)
    tcp_socket.sendall(nome_to_bytes) # CLIENTE ENVIANDO Segundo Datagrama
    print(f"[OK] Segundo datagrama enviado: nome = {nome_file}\n")

    # 0 ⭢ Arquivo não existe | 1 ⭢ Arquivo existe
    resposta = tcp_socket.recv(1) # CLIENTE RECEBENDO 1 byte (0 ⭢ b'\x00') ou (1 ⭢ b'\x01')

    if resposta == b'\x00': # Arquivo não existe (b'\x00')
        print("Arquivo não existe no SERVIDOR.")
        tcp_socket.close()
        exit()
    else: # Arquivo existe (b'\x01')
        print("Arquivo existe no SERVIDOR, recebendo...")

    # 4 bytes: Tamanho do arquivo
    tamanho_bytes = tcp_socket.recv(4) # CLIENTE RECEBENDO 4 Bytes
    tamanho = int.from_bytes(tamanho_bytes, "big") # INTEIRO (Inteiro ⭠ Bytes)

    # Recebe o conteúdo do arquivo em uma sequência de datagramas de até 4096 Bytes
    conteudo = b""
    while len(conteudo) < tamanho:
        bloco = tcp_socket.recv(4096)  # Recebe até 4096 bytes
        conteudo = conteudo + bloco  # Adiciona os bytes recebidos ao conteúdo total

    # Salva o arquivo
    with open(os.path.join("cliente","dowloads", nome_file), "wb") as f: # with open(nome_file, "wb") as f:
        f.write(conteudo)

    print(f"Arquivo '{nome_file}' salvo com sucesso!")
    tcp_socket.close()

# REQUISIÇÃO DE LISTAGEM (Se Operacao == 20)
elif operacao == 20:
   
    status = tcp_socket.recv(1) # CLIENTE RECEBE 

    if status == b'\x00':
        print("Erro ao obter listagem do servidor.")
    else:
        # Recebe tamanho do JSON
        tamanho_bytes = tcp_socket.recv(4)
        tamanho = int.from_bytes(tamanho_bytes, "big")
        
        # Recebe o conteúdo do arquivo em uma sequência de datagramas de até 4096 Bytes
        dados = b""
        while len(dados) < tamanho:
            bloco = tcp_socket.recv(4096)  # Recebe até 4096 bytes
            dados = dados + bloco  # Adiciona os bytes recebidos ao conteúdo total
            
        dados_str = dados.decode("utf-8") # STRING (String ⭠ Bytes)
        lista = json.loads(dados_str) # LISTA (Lista ⭠ Json(String))

        print("\nArquivos disponíveis no servidor:\n")
        for arquivo in lista:
            print(f"- {arquivo['nome']} ({arquivo['tamanho']} bytes)")
else:
    print("Operação Inválida")

tcp_socket.close()
