import string

letras = string.ascii_uppercase

def cifrar(mensaje, clave, t):
    cifrado = ""
    count = 0

    for i in range(len(mensaje)):
        indice_clave = letras.find(clave[count])
        indice_mensaje = letras.find(mensaje[i])
        cifrado += letras[(indice_clave + indice_mensaje) % 26]
        count = (count + 1) % len(clave)
        if (i + 1) % t == 0 and i != 0:
            cifrado += " "
    return cifrado

def descifrar(cifrado, clave, t):
    descifrado = ""
    count = 0
    cifrado = cifrado.replace(" ", "") 

    for i in range(len(cifrado)):
        indice_clave = letras.find(clave[count])
        indice_cifrado = letras.find(cifrado[i])
        descifrado += letras[(indice_cifrado - indice_clave + 26) % 26]
        count = (count + 1) % len(clave)
        if (i + 1) % t == 0 and i != 0:
            descifrado += " "
    return descifrado

def main():
    print("=== Cifrado Vigenère ===")
    opcion = input("¿Qué deseas hacer? (C)ifrar o (D)escifrar: ").strip().upper()

    if opcion not in ['C', 'D']:
        print("Opción inválida. Usa 'C' para cifrar o 'D' para descifrar.")
        return

    texto = input("Introduce el texto: ").upper().replace(" ", "")
    clave = input("Introduce la clave: ").strip().upper()
    t = int(input("Tamaño de grupo (para separar con espacios): "))

    if opcion == 'C':
        resultado = cifrar(texto, clave, t)
        print("\nTexto cifrado:")
    else:
        resultado = descifrar(texto, clave, t)
        print("\nTexto descifrado:")

    print(resultado)

if __name__ == "__main__":
    main()
