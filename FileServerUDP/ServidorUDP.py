import socket
import os

HOST = '192.168.56.1' # IP do servidor (IP do HOST rodando o servidor)
PORT = 20000          # Definindo a porta     

# Criando o socket UDP
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((HOST, PORT))

print("-----------------------------------------------------")
print("|Servidor UDP de arquivos iniciado na porta 20000...|")
print("-----------------------------------------------------\n")

# Loop principal
while True:
    print("Aguardando arquivo...\n")

    # Primeiro Datagrama (Tamanho do nome do arquivo ⭢ 1 Byte)
    primeiro_data, endereco_cliente = udp_socket.recvfrom(1) # Servidor espera receber 1 Byte (Primeiro Datagrama)
    tamanho_nome = int.from_bytes(primeiro_data, "big") # Converte o 1 Byte recebido em um inteiro.

    # Segundo Datagrama (Nome do arquivo sendo solicitado. ⭢ Vários Bytes)
    segundo_data, endereco_cliente = udp_socket.recvfrom(tamanho_nome) # Serviodor espera receber vários Byte (Segundo Datagrama)
    nome_arquivo = segundo_data.decode("utf-8") # Converte vários Bytes recebidos em uma string.

    print(f"Cliente {endereco_cliente} solicitou: {nome_arquivo}")

    # Caminho do arquivo (files/"nome do arquivo dado pelo usuário")
    caminho_arquivo = os.path.join("files", nome_arquivo) # nome_arquivo = vários bytes convertidos em string

    # Verifica se o arquivo existe
    if not os.path.exists(caminho_arquivo):
        print("Arquivo não encontrado.")
        udp_socket.sendto(b'\x00', endereco_cliente)  # Envia 0 → Arquivo não existe
       
    else: 
        print("Arquivo encontrado. Enviando...\n") 
        udp_socket.sendto(b'\x01', endereco_cliente) # Envia 1 → arquivo existe

        # Obtém tamanho do arquivo
        tamanho_arquivo = os.path.getsize(caminho_arquivo)
    
        # Envia tamanho do arquivo (4 bytes - big-endian)
        tamanho_bytes = tamanho_arquivo.to_bytes(4, byteorder="big")
        udp_socket.sendto(tamanho_bytes, endereco_cliente)

        # Envia o conteudos em blocos de 4096
        with open(caminho_arquivo, "rb") as f:
            while True:
                bloco = f.read(4096)
                if not bloco:
                    break
                else:
                    udp_socket.sendto(bloco, endereco_cliente)

        print("Arquivo enviado com sucesso.")
