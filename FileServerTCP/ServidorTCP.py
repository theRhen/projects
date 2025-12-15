import socket
import os
import json

HOST = '192.168.56.1' # IP do servidor (IP do HOST servidor)
PORT = 20000          # Definindo a porta     

# Obtém o diretório absoluto onde do codigo
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Pasta onde o código esta rodando
FILES_DIR = os.path.join(BASE_DIR, "files")           # Pasta "files" dentro da pasta onde o código esta rodando

# Criando o socket TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Socket TCP (STREAM)
tcp_socket.bind((HOST, PORT))                                  # Ligando o socket a porta
tcp_socket.listen(1)                                           # Máximo de conexões enfileiradas

print("------------------------------------------------------")
print("|  Servidor TCP de arquivos iniciado na porta 20000  |")
print("------------------------------------------------------\n")

# LOOP PRINCIPAL
while True:
    print("Aguardando arquivo...\n")
    con, endereco_cliente = tcp_socket.accept() # Aceita a conexão com o cliente
    
    # Datagrama operação
    operacao_bytes = con.recv(1) # SERVIDOR RECEBENDO 1 Byte (Operação Datagrama)
    operacao = int.from_bytes(operacao_bytes, "big") # Inteiro (Inteiro ⭠ Bytes)
    
    # REQUISIÇÃO DE DOWLOAD (Se Operacao == 10)
    if operacao == 10:
        
        # Datagrama 1 (Tamanho do nome do arquivo 1 BYTE)
        primeiro_data = con.recv(1) # SERVIDOR RECEBENDO 1 Byte (Primeiro Datagrama)
        tamanho_nome = int.from_bytes(primeiro_data, "big") # INTEIRO (Inteiro ⭠ Bytes)

        # Datagrama 2 (Nome do arquivo VÁRIOS BYTES)
        segundo_data = con.recv(tamanho_nome) # SERVIDOR RECEBENDO vários Bytes (Segundo Datagrama)
        nome_arquivo = segundo_data.decode("utf-8") # STRING (String ⭠ Bytes)

        print(f"Cliente: {endereco_cliente} | Solicitou: {nome_arquivo}\n")

        # Caminho do arquivo (files/"nome do arquivo dado pelo usuário")
        caminho_arquivo = os.path.join(FILES_DIR, nome_arquivo) 

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
            
    # REQUISIÇÃO DE LISTAGEM (Se Operacao == 20)
    elif operacao == 20:
        print(f"Cliente: {endereco_cliente} | Solicitou listagem de arquivos\n")

        lista_arquivos = []

        for nome in os.listdir(FILES_DIR):
            caminho = os.path.join(FILES_DIR, nome)

            if os.path.isfile(caminho):
                tamanho = os.path.getsize(caminho)
                lista_arquivos.append({
                    "nome": nome,
                    "tamanho": tamanho
                })
                
        # Converte lsta para json
        json_lista = json.dumps(lista_arquivos) # JSON (Json(String) ⭠ Lista)
        json_bytes = json_lista.encode("utf-8") # BYTES (Bytes ⭠ Json(String))

        con.sendall(b'\x01') # SERVIDOR ENVIANDO 1 → Listagem será enviada
        
        # Calcula o tamanho da lista em bytes "Percorre cada caracter"
        tamanho_json = len(json_bytes) # INTEIRO (Inteiro ⭠ Bytes) 
        json_to_bytes = tamanho_json.to_bytes(4, "big") # BYTES (Bytes ⭠ Inteiro)
        con.sendall(json_to_bytes) # SERVIDOR ENVIANDO 4 Bytes

        con.sendall(json_bytes) # SERVIDOR ENVIANDO Listagem em formato json

        print("Listagem enviada com sucesso.\n")
        print("------------------------------------------------------\n")
                
    con.close()
