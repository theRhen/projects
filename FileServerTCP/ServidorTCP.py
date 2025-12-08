import socket
import os

HOST = '192.168.56.1' # IP do servidor (IP do HOST servidor)
PORT = 20000          # Definindo a porta     

# Criando o socket TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind((HOST, PORT)) # Ligando o socket a porta
tcp_socket.listen(1)          # Máximo de conexões enfileiradas

print("------------------------------------------------------")
print("|  Servidor TCP de arquivos iniciado na porta 20000  |")
print("------------------------------------------------------\n")

# Loop principal
while True:
    print("Aguardando arquivo...\n")
    con, endereco_cliente = tcp_socket.accept() # Aceita a conexão com o cliente
    
    # Datagrama 1 (Tamanho do nome do arquivo 1 BYTE)
    primeiro_data = con.recv(1) # SERVIDOR RECEBENDO 1 Byte (Primeiro Datagrama)
    tamanho_nome = int.from_bytes(primeiro_data, "big") # INTEIRO (Inteiro ⭠ Bytes)

    # Datagrama 2 (Nome do arquivo VÁRIOS BYTES)
    segundo_data = con.recv(tamanho_nome) # SERVIDOR RECEBENDO vários Bytes (Segundo Datagrama)
    nome_arquivo = segundo_data.decode("utf-8") # STRING (String ⭠ Bytes)

    print(f"Cliente: {endereco_cliente} | Solicitou: {nome_arquivo}\n")

    # Caminho do arquivo (files/"nome do arquivo dado pelo usuário")
    caminho_arquivo = os.path.join("files", nome_arquivo) 

    # Verifica se o arquivo existe
    if not os.path.exists(caminho_arquivo): 
        print("Arquivo não encontrado.\n")
        con.sendall(b'\x00') # SERVIDOR ENVIANDO 0 → Arquivo não existe
        print("------------------------------------------------------\n")
       
    else: 
        print("Arquivo encontrado. Enviando...") 
        con.sendall(b'\x01') # SERVIDOR ENVIANDO 1 → Arquivo existe

        # Obtém tamanho do arquivo
        tamanho_arquivo = os.path.getsize(caminho_arquivo)
    
        # Envia tamanho do arquivo (4 bytes - big-endian)
        tamanho_bytes = tamanho_arquivo.to_bytes(4, byteorder="big")
        con.sendall(tamanho_bytes) # SERVIDOR ENVIANDO 4 Bytes

        # Envia o conteudos em blocos de 4096
        with open(caminho_arquivo, "rb") as f:
            while True:
                bloco = f.read(4096)
                if not bloco:
                    break
                else:
                    con.sendall(bloco)

        print("Arquivo enviado com sucesso.\n")
        print("------------------------------------------------------\n")
