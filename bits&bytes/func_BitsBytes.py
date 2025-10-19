#CONVERTER BITS PARA BYTES
def bits_para_bytes(bits):
    return bits / 8

#CONVERTER BYTES PARA BITS
def bytes_para_bites(bytes):
    return bytes * 8

#ENTRADAS
bits = int(input("BITS → BYTES: "))
print(bits, "bits", "=", bits_para_bytes(bits), "bytes", "\n")

bytes = int(input("BYTES → BITS: "))
print(bytes, "bytes", "=", bytes_para_bites(bytes), "bits")
