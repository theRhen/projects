import msvcrt

def formatar_valor(digitos: str) -> str:
    if digitos == "":
        return "R$ 0,00"
    valor = int(digitos) / 100
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def maquininha() -> str:
    print("Valor (ENTER para confirmar):")
    digitos = ""
    while True:
        tecla = msvcrt.getch()

        if tecla == b'\r':  # ENTER confirma
            break
        elif tecla == b'\x08':  # BACKSPACE apaga
            digitos = digitos[:-1]
        elif tecla.isdigit():  # só aceita números
            digitos += tecla.decode()

        # Atualiza valor na mesma linha
        print("\r" + " " * 20, end="")
        print("\r" + formatar_valor(digitos), end="")

    return formatar_valor(digitos)
