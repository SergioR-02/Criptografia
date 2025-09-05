import string

# Caracteres permitidos: letras, dígitos, puntuación y espacio
listChar = list(string.ascii_letters + string.digits + string.punctuation + " ")

def encryption(plaintext, key):
    ciphertext = ""
    if len(plaintext) == len(key):
        for i in range(len(plaintext)):
            try:
                index = (listChar.index(plaintext[i]) + listChar.index(key[i])) % len(listChar)
                ciphertext += listChar[index]
            except ValueError:
                return "Caracter no permitido"
    return ciphertext

def decryption(ciphertext, key):
    plaintext = ""
    if len(ciphertext) == len(key):
        for i in range(len(ciphertext)):
            try:
                index = (listChar.index(ciphertext[i]) - listChar.index(key[i])) % len(listChar)
                plaintext += listChar[index]
            except ValueError:
                return "Caracter no permitido"
    return plaintext

def main():
    # Mensaje y clave deben tener la misma longitud
    msg = "Hola mundo encriptado 123!"
    key = "ClaveSeguraDePruebaXyZ8901" 

    if len(msg) != len(key):
        print("ERROR: El mensaje y la clave deben tener la misma longitud.")
        return

    encrypted = encryption(msg, key)
    print("Mensaje original:", msg)
    print("Clave:           ", key,)
    print("Cifrado:         ", encrypted,"\n")

    decrypted = decryption(encrypted, key)
    print("Descifrado:      ", decrypted)

main()
