#CONVERTER DECIMAL PARA BITS
def decimal_para_bits(decimal):
    return bin(decimal)

#ENTRADA
decimal = int(input("DEC → BIT: "))
print(decimal, "(10)", "=", decimal_para_bits(decimal), "(2)")
