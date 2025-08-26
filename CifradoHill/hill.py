# Calcula el determinante de una matriz 2x2 en Z_26
def determinante(matriz):
  a, b = matriz[0]
  c, d = matriz[1]
  return (a * d - b * c) % 26

# Algoritmo de Euclides para obtener el MCD
def gcd(a, b):
  while b:
    a, b = b, a % b
  return a

# Verifica si el determinante tiene inverso modular en Z_26
def tiene_inverso_modular(det, modulo=26):
  return gcd(det, modulo) == 1

# Algoritmo extendido de Euclides
def eea(a, b):
  if b == 0:
    return a, 1, 0
  d, x1, y1 = eea(b, a % b)
  x, y = y1, x1 - (a // b) * y1
  return d, x, y

# Calcula el inverso modular si existe
def inverso_mod(a, mod=26):
  d, x, _ = eea(a, mod)
  return x % mod if d == 1 else None

# Devuelve la matriz adjunta (cofactores y traspuesta simplificada)
def adjunta(m):
  return [[m[1][1], -m[0][1]],
          [-m[1][0], m[0][0]]]

# Calcula la inversa modular de una matriz 2x2 en Z_26
def inversa_modulo(m):
  det = determinante(m)
  inv_det = inverso_mod(det)
  if inv_det is None:
    return None
  adj = adjunta(m)
  return [[(inv_det * adj[i][j]) % 26 for j in range(2)] for i in range(2)]

# Convierte texto a lista de números (A=0, ..., Z=25), agrega X si es impar
def texto_a_numeros(texto):
  texto = texto.upper().replace(" ", "")
  if len(texto) % 2 != 0:
    texto += "X"
  return [ord(c) - ord('A') for c in texto]

# Convierte números (0–25) de vuelta a texto
def numeros_a_texto(numeros):
  return ''.join(chr(n % 26 + ord('A')) for n in numeros)

# Aplica la matriz sobre los pares de números (bloques) del mensaje
def procesar_bloques(numeros, matriz):
  resultado = []
  for i in range(0, len(numeros), 2):
    a, b = numeros[i], numeros[i + 1]
    x = (matriz[0][0] * a + matriz[1][0] * b) % 26
    y = (matriz[0][1] * a + matriz[1][1] * b) % 26
    resultado.extend([x, y])
  return resultado

# Función principal para interacción con el usuario
def main():
  opcion = input("¿Desea cifrar (C) o descifrar (D)?: ").strip().upper()
  while opcion not in ["C", "D"]:
    opcion = input("Opción inválida. Escriba C para cifrar o D para descifrar: ").strip().upper()

  mensaje = input("Ingrese el mensaje (solo letras): ").strip().upper()
  numeros = texto_a_numeros(mensaje)

  # Ingreso de matriz con validación
  while True:
    print("Ingrese los valores de la matriz 2x2 por filas, separados por espacios:")
    try:
      matriz = [list(map(int, input(f"Fila {i+1}: ").split())) for i in range(2)]
      if all(all(0 <= x < 26 for x in fila) and len(fila) == 2 for fila in matriz):
        det = determinante(matriz)
        if tiene_inverso_modular(det):
          break
        else:
          print("No tiene inverso modular. No es válida para el cifrado Hill.\n")
      else:
        print("Los valores deben ser enteros entre 0 y 25, y deben ser dos por fila.\n")
    except ValueError:
      print("Entrada inválida. Asegúrese de ingresar solo números.\n")

  if opcion == "D":
    matriz = inversa_modulo(matriz)  # Solo se invierte si se desea descifrar


  resultado = procesar_bloques(numeros, matriz)
  texto_resultado = numeros_a_texto(resultado)

  print(f"\nResultado: {texto_resultado}")

main()
