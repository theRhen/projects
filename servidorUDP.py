import socket
import os
import struct

HOST = '192.168.56.1'   # IP do servidor
PORT = 20000

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
    primeiro_data, cliente = udp_socket.recvfrom(1)
    tamanho_nome = int.from_bytes(primeiro_data, "big")

    # Segundo Datagrama (Nome do arquivo sendo solicitado.)
    segundo_data, _ = udp_socket.recvfrom(tamanho_nome)
    nome_arquivo = segundo_data.decode("utf-8")

    print(f"Cliente {cliente} solicitou: {nome_arquivo}")

    # Caminho completo do arquivo dentro da pasta "files/"
    caminho_arquivo = os.path.join("files", nome_arquivo)

    # Verifica se o arquivo existec
    if not os.path.exists(caminho_arquivo):
        print("Arquivo não encontrado.\n")
        # Envia 0 → arquivo não existe
        udp_socket.sendto(b'\x00', cliente)
        continue

    # ===== ARQUIVO EXISTE =====
    print("Arquivo encontrado. Enviando...\n")
    # Envia 1 → arquivo existe
    udp_socket.sendto(b'\x01', cliente)

    # Obtém tamanho do arquivo
    tamanho_arquivo = os.path.getsize(caminho_arquivo)

    # Envia tamanho do arquivo (4 bytes - big-endian)
    tamanho_bytes = struct.pack("!I", tamanho_arquivo)
    udp_socket.sendto(tamanho_bytes, cliente)

    # ===== ENVIO DO CONTEÚDO EM BLOCOS DE 4096 =====
    with open(caminho_arquivo, "rb") as f:
        while True:
            bloco = f.read(4096)
            if not bloco:
                break
            udp_socket.sendto(bloco, cliente)

    print("Arquivo enviado com sucesso.\n")
