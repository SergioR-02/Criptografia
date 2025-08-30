

# Rota la matriz hacia la derecha
def right(matrix):
  rotated_matrix = []
  for column in range(len(matrix[0])):
    row = []
    for row_index in range(len(matrix)-1, -1, -1):
      row.append(matrix[row_index][column])
    rotated_matrix.append(row)
  return rotated_matrix

# Rota la matriz hacia la izquierda
def left(matrix):
  rotated_matrix = []
  for column in range(len(matrix)-1, -1, -1):
    row = []
    for row_index in range(len(matrix)):
      row.append(matrix[row_index][column])
    rotated_matrix.append(row)
  return rotated_matrix

# Calcula el número recomendado de agujeros según el tamaño de la matriz
def num_holes(n):
  total_holes = 0
  if n % 2 == 0:
    for size in range(n, 0, -2):
      total_holes += size - 1
  else:
    for size in range(n, 0, -2):
      if size == 1:
        total_holes += 1
        break
      total_holes += size - 1
  return total_holes

# Cifra el mensaje usando la rejilla giratoria
def encryption(holes_matrix, message, clockwise_direction):
  matrix_size = len(holes_matrix)
  cipher_matrix = [matrix_size * [0] for _ in range(matrix_size)]
  encrypted_message = ""
  character_index = 0
  
  for rotation in range(4):
    for row in range(matrix_size):
      for column in range(matrix_size):
        if holes_matrix[row][column] == "#":
          cipher_matrix[row][column] = message[character_index]
          character_index += 1
        if rotation == 3:
          encrypted_message += cipher_matrix[row][column]
    if rotation == 3:
      break
    
    # Rotar según la dirección especificada
    if clockwise_direction == 1:
      holes_matrix = right(holes_matrix)
    else:
      holes_matrix = left(holes_matrix)
  
  print("\nMensaje cifrado:", encrypted_message, "\n")
  return encrypted_message

# Descifra el mensaje usando la rejilla giratoria
def decryption(holes_matrix, encrypted_message, clockwise_direction):
  matrix_size = len(holes_matrix)
  # Crear matriz con el mensaje cifrado
  cipher_matrix = []
  message_index = 0
  for row in range(matrix_size):
    matrix_row = []
    for column in range(matrix_size):
      matrix_row.append(encrypted_message[message_index])
      message_index += 1
    cipher_matrix.append(matrix_row)
  
  decrypted_message = ""
  
  for rotation in range(4):
    for row in range(matrix_size):
      for column in range(matrix_size):
        if holes_matrix[row][column] == "#":
          decrypted_message += cipher_matrix[row][column]
    
    if rotation < 3: 
      if clockwise_direction == 1:
        holes_matrix = right(holes_matrix)
      else:
        holes_matrix = left(holes_matrix)
  
  print("\nMensaje descifrado:", decrypted_message, "\n")
  return decrypted_message



def hole(matrix, total_holes):
  print("Ingrese las coordenadas de los hoyos (fila columna, comenzando desde 0):")
  for hole_number in range(total_holes):
    while True:
      try:
        coordinates = [int(x) for x in input(f"Coordenadas del hoyo {hole_number + 1} (fila columna): ").split()]
        if len(coordinates) == 2 and 0 <= coordinates[0] < len(matrix) and 0 <= coordinates[1] < len(matrix):
          matrix[coordinates[0]][coordinates[1]] = "#"
          break
        else:
          print(f"Coordenadas inválidas. Deben estar entre 0 y {len(matrix)-1}. Intente de nuevo.")
      except (ValueError, IndexError):
        print("Error en el formato. Ingrese dos números separados por espacio.")

# Función principal que controla el flujo del programa
def main():
  print("=== ALGORITMO TURNING GRILLE ===")
  
  matrix_size = int(input("Ingrese el tamaño de la retícula: "))
  
  # Dirección de rotación
  print("Dirección de rotación:\n1 - Sentido de las manecillas del reloj\n0 - Sentido contrario a las manecillas del reloj")
  clockwise_direction = int(input("Ingrese la dirección (1 o 0): "))
  
  #(cifrado o descifrado)
  print("\nModo de operación:")
  print("1 - Cifrado")
  print("0 - Descifrado")
  mode = int(input("Ingrese el modo (1 ó 0): "))

  holes_matrix = [matrix_size * [0] for _ in range(matrix_size)]
  recommended_holes = num_holes(matrix_size)
  print(f"\nSe recomienda usar {recommended_holes} hoyos para un funcionamiento óptimo.")
  hole_count = int(input("Ingrese la cantidad de hoyos: "))
  
  hole(holes_matrix, hole_count)
  
  
  # Mensaje a (de)cifrar
  if mode == 1:  # Cifrado
    message = input("Ingrese el mensaje a cifrar: ").replace(" ", "").upper()
    required_length = hole_count * 4
    if len(message) > required_length:
      print(f"Mensaje muy largo. Se truncará a {required_length} caracteres.")
      message = message[:required_length]
    elif len(message) < required_length:
      print(f"Mensaje muy corto. Se rellenará con 'X' hasta {required_length} caracteres.")
      message += 'X' * (required_length - len(message))

    result = encryption(holes_matrix, message, clockwise_direction)
    
  else:  # Descifrado
    encrypted_message = input("Ingrese el mensaje cifrado: ").replace(" ", "").upper()
    expected_length = matrix_size * matrix_size
    if len(encrypted_message) != expected_length:
      print(f"El mensaje cifrado debe tener exactamente {expected_length} caracteres.")
      return
    
    result = decryption(holes_matrix, encrypted_message, clockwise_direction)
    

main()



