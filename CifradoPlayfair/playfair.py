
#Crear la matriz para el cifrado
def crearMatriz(key):
  #Se eliminan los espacios y las j por las i
  cadena=key.upper().replace(" ","").replace("j","i")
  cadenaCompleta=""

  #Se eliminan las letras repetidas
  for i in cadena:
    if i not in cadenaCompleta:
      cadenaCompleta+=i

  #Se agrega el abcedarios restante 
  for i in range(65,91):
    if chr(i) not in cadenaCompleta and i!=74:
      cadenaCompleta+=chr(i)

  #Se pasa la cadena a Matriz
  matriz=[]
  for i in range(0,25,5):
    matriz.append([x for x in cadenaCompleta[i:i+5]])
  return matriz

#Darle el formato al mensaje para encriptarlo
def mensajeFormato(mensaje):
  new=""
  mensaje=mensaje.upper().replace(" ","").replace("j","i")
  pareja=False

  #Se agrega una X si ambas letras en una pareja son iguales 
  for i in range(len(mensaje)):
    if pareja and len(new)>0 :
      if mensaje[i]==new[-1]:
        new+="X" + mensaje[i]
      else:
        new+=mensaje[i]
        pareja=False
    else:
      new+= mensaje[i]
      pareja=True

  #Completar la pareja final si es necesario
  if len(new)%2!=0:
    new+="X"
  return new

#Obtener la posicion de elemento en la matriz en una tupla x,y
def pocision(n,matriz):
  for i in range(len(matriz)):
    for j in range(len(matriz[i])):
      if n == matriz[i][j]:
        return i,j

#Cifrar dado los diferentes casos segun la posicion de las parejas
def cifrar(mensaje, matriz):
  resultado=""
  for i in range(0,len(mensaje),2):
    fila1,columna1=pocision(mensaje[i],matriz)
    fila2,columna2=pocision(mensaje[i+1],matriz)
    
    if fila1!=fila2 and columna1!=columna2:
      resultado+=matriz[fila1][columna2]+matriz[fila2][columna1]

    elif fila1==fila2:
      resultado+=matriz[fila1][(columna1+1)%5]+matriz[fila2][(columna2+1)%5]
    
    elif columna1==columna2:
      resultado+=matriz[(fila1+1)%5][columna1]+matriz[(fila2+1)%5][columna2]

  return resultado

#Descifrar dado los diferentes casos segun la posicion de las parejas
def descifrar(mensaje,matriz):
  resultado=""
  for i in range(0,len(mensaje),2):
    fila1,columna1=pocision(mensaje[i],matriz)
    fila2,columna2=pocision(mensaje[i+1],matriz)
    
    if fila1!=fila2 and columna1!=columna2:
      resultado+=matriz[fila1][columna2]+matriz[fila2][columna1]

    elif fila1==fila2:
      resultado+=matriz[fila1][(columna1-1) % 5]+matriz[fila2][(columna2-1) % 5]
    
    elif columna1==columna2:
      resultado+=matriz[(fila1-1) % 5][columna1]+matriz[(fila2-1) % 5][columna2]
  
  return resultado

def limpiarMensaje(mensaje):
    # Dividir en parejas de dos en dos
    parejas = [mensaje[i:i+2] for i in range(0, len(mensaje), 2)]
    resultado = ""

    for idx, par in enumerate(parejas):
        if len(par) == 2:
            a, b = par[0], par[1]
            resultado += a

            # Si es X de relleno
            if b == 'X':
                # No es ultima pareja y la siguiente empieza igual que a -> saltar la X
                if idx < len(parejas)-1 and parejas[idx+1][0] == a:
                    continue
                # Si es la ultima pareja, también eliminar la X
                elif idx == len(parejas)-1:
                    continue
                # En otro caso, mantener la X
                else:
                    resultado += b
            else:
                resultado += b
        else:
            # Pareja incompleta (última letra solitaria)
            resultado += par

    return resultado


def main():
  opcion = input("Playfair, elija una opción 1 o 2\n1. Cifrar\n2. Descifrar\n> ")

  if opcion == '1':
    message = input("Ingrese el mensaje a cifrar: ")
    key     = input("Ingrese la clave: ")
    matriz    = crearMatriz(key)          
    formateado = mensajeFormato(message)  
    cifrado = cifrar(formateado, matriz) 
    print("\nTexto cifrado:", cifrado )


  elif opcion == '2':
    message = input("Ingrese el mensaje a descifrar: ")
    key     = input("Ingrese la clave: ")

    matriz    = crearMatriz(key)          
    formateado = mensajeFormato(message)  
    descifrado = descifrar(formateado, matriz) 
    print("\nTexto descifrado:", limpiarMensaje(descifrado))
  else:
    print("Opción no válida")

if __name__ == "__main__":
    main()

