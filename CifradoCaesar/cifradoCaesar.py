import string
lista=string.ascii_uppercase


def cifrar(mensaje, k):
  mensaje = mensaje.upper().replace(" ", "")
  cifrado=""
  count=1
  for i in mensaje:
    if (i.isalpha() == False):
      pass
    else:
      a= ord(i) - 65
      cifrado += lista[(a + k) % 26]
      if count==5:
        cifrado+=" "
        count=1
      else:
        count+=1
  return(cifrado)

def descifrar(mensaje, k):
  mensaje = mensaje.upper().replace(" ", "")
  cifrado=""
  for i in mensaje:
    if (i.isalpha() == False):
      pass
    else:
      a= ord(i) - 65
      cifrado += lista[(a - k) % 26]
  return(cifrado)

def main():
  while True:
    print("\nElige una opción:")
    print("1. Cifrar un mensaje")
    print("2. Descifrar un mensaje")
    print("3. Salir")
    opcion = input("Opción: ")

    if opcion == "1":
      mensaje = input("Ingresa el mensaje a cifrar: ")
      k = int(input("Ingresa la permutación (número): "))
      mensaje_cifrado = cifrar(mensaje, k)
      print(f"Mensaje cifrado: {mensaje_cifrado}")
    elif opcion == "2":
      mensaje = input("Ingresa el mensaje a descifrar: ")
      k = int(input("Ingresa la permutación (número): "))
      mensaje_descifrado = descifrar(mensaje, k)
      print(f"Mensaje descifrado: {mensaje_descifrado}")
    elif opcion == "3":
      print("Saliendo del programa...")
      break
    else:
      print("Opción no válida. Intenta de nuevo.")

# Llamar a la función main
main()