import socket

HOST = '192.168.56.1' # IP do cliente (IP do HOST cliente)
PORT = 20000          # Definindo a porta

# Criando o socket UDP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect((HOST, PORT))

# Entrada
nome_file = input("Nome do arquivo sendo solicitado (ex: exemplo.txt): ")
print()
nome_bytes = nome_file.encode('utf-8') # Converte o nome para bytes (UTF-8) (ex: exemplo.txt ⭢ b'exemplo.txt')
tamanho_file = len(nome_bytes) # Calcula o tamanho em bytes "Percorre cada caracter" (ex: exemplo.txt ⭢ 11)

# Datagrama 1
tamanho_to_byte = tamanho_file.to_bytes(1, "big") # Primeiro Datagrama (Tamanho do nome do arquivo ⭢ 1 Byte)
tcp_socket.sendall(tamanho_to_byte) # Enviando Primeiro Datagrama
print(f"[OK] Primeiro datagrama enviado: tamanho = {tamanho_file} byte(s)")

# Datagrama 2
nome_to_bytes = nome_bytes # Segundo Datagrama (Nome do arquivo sendo solicitado.)
tcp_socket.sendall(nome_to_bytes) # Enviando Segundo Datagrama
print(f"[OK] Segundo datagrama enviado: nome = {nome_file}\n")

resposta = tcp_socket.recv(1) # recebe 1 byte + endereço do cliente
resposta_bytes = resposta  

# 0 ⭢ Arquivo não existe | 1 ⭢ Conteúdo do arquivo será enviado
if resposta == b'\x00': # Arquivo não existe
    print("Arquivo não existe no SERVIDOR.")
    tcp_socket.close()
    exit()
else: # Arquivo existe
    print("Arquivo existe no SERVIDOR, recebendo...")

# 4 bytes: Tamanho do arquivo
tamanho_bytes = tcp_socket.recv(4) # recebe 1 byte
tamanho = int.from_bytes(tamanho_bytes, "big") # converte bytes em inteiro

# Recebe o conteúdo do arquivo em uma sequência de datagramas de até 4096 bytes
conteudo = b""
while len(conteudo) < tamanho:
    bloco = tcp_socket.recv(4096)  # recebe até 4096 bytes
    conteudo = conteudo + bloco  # adiciona os bytes recebidos ao conteúdo total

# Salva o arquivo
with open(nome_file, "wb") as f: # 
    f.write(conteudo)

print(f"Arquivo '{nome_file}' salvo com sucesso!")
tcp_socket.close()
