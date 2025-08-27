import random

# Layout estático
layout_cifrado = {
    'A': [9, 12, 33, 47, 53, 67, 78, 92],
    'B': [48, 81],
    'C': [13, 41, 62],
    'D': [1, 3, 45, 79],
    'E': [14, 16, 24, 44, 46, 55, 57, 64, 74, 82, 87, 88],
    'F': [10, 31],
    'G': [6, 25],
    'H': [23, 39, 50, 56, 65, 68],
    'I': [32, 70, 73, 83, 88, 93],
    'J': [15],
    'K': [4],
    'L': [26, 37, 51, 84],
    'M': [22, 27],
    'N': [18, 58, 59, 66, 71, 91],
    'O': [0, 5, 17, 54, 72, 90, 99],
    'P': [38, 95],
    'Q': [94],
    'R': [29, 35, 40, 42, 77, 80],
    'S': [11, 19, 36, 76, 86, 96],
    'T': [17, 20, 30, 43, 49, 69, 75, 85, 97],
    'U': [8, 61, 63],
    'V': [34],
    'W': [60, 89],
    'X': [28],
    'Y': [21, 52],
    'Z': [2]
}

# Invertir layout para descifrar
layout_descifrado = {}
for letra, codigos in layout_cifrado.items():
    for codigo in codigos:
        layout_descifrado[codigo] = letra

def cifrar(texto_claro):
    texto_claro = texto_claro.upper()
    mensaje_cifrado = []
    for letra in texto_claro:
        if letra in layout_cifrado:
            codigo = random.choice(layout_cifrado[letra])
            mensaje_cifrado.append(str(codigo))
        else:
            print(f"[Advertencia] Caracter ignorado: {letra}")
    return ' '.join(mensaje_cifrado)

def descifrar(mensaje_cifrado):
    try:
        codigos = list(map(int, mensaje_cifrado.strip().split()))
        mensaje_descifrado = ''
        for codigo in codigos:
            letra = layout_descifrado.get(codigo, '?')
            mensaje_descifrado += letra
        return mensaje_descifrado
    except ValueError:
        return "[Error] Formato incorrecto. Asegúrese de ingresar números separados por espacios."

def main():
    while True:
        print("\n--- CIFRADO HOMOFÓNICO ---")
        print("1. Cifrar mensaje")
        print("2. Descifrar mensaje")
        print("3. Salir")
        opcion = input("Seleccione una opción (1/2/3): ").strip()

        if opcion == '1':
            texto = input("Ingrese el texto claro: ")
            resultado = cifrar(texto)
            print("Mensaje cifrado:", resultado)
        elif opcion == '2':
            texto = input("Ingrese el mensaje cifrado (números separados por espacios): ")
            resultado = descifrar(texto)
            print("Mensaje descifrado:", resultado)
        elif opcion == '3':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()
