import pyDes
import base64
from PIL import Image
import io
import os
import sys
import glob

def image_to_bits(image_path):
    # Paso 1: Convierte una imagen a representación de bits

    print(f"Leyendo imagen: {image_path}")
    
    # Leer el archivo de imagen como bytes
    with open(image_path, 'rb') as file:
        image_bytes = file.read()
    
    print(f"Tamaño original: {len(image_bytes)} bytes")
    return image_bytes

def pad_data(data):
    # Función auxiliar: DES requiere que los datos sean múltiplos de 8 bytes
    
    # Calcular cuántos bytes necesitamos agregar
    padding_length = 8 - (len(data) % 8)
    if padding_length == 8:
        padding_length = 0
    # Agregar padding
    padded_data = data + bytes([padding_length] * padding_length)
    print(f"Padding agregado: {padding_length} bytes")
    return padded_data, padding_length

def remove_padding(data, original_padding):
    # Función auxiliar: Remover el padding después del descifrado

    if original_padding > 0:
        return data[:-original_padding]
    return data

def encrypt_with_des(data, key):
    # Paso 2: Cifrar los datos usando DES
    
    print("Iniciando cifrado DES...")
    
    # Crear objeto DES con la clave
    des_cipher = pyDes.des(key, pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    
    # Cifrar los datos
    encrypted_data = des_cipher.encrypt(data)
    print(f"Cifrado completado. Tamaño cifrado: {len(encrypted_data)} bytes")
    
    return encrypted_data

def encode_base64(data):
    # Paso 3: Codificar en Base64
    
    print("Codificando en Base64...")
    encoded_data = base64.b64encode(data)
    print(f"Codificación Base64 completada. Tamaño: {len(encoded_data)} caracteres")
    return encoded_data

def decode_base64(encoded_data):
    # Paso 4: Decodificar de Base64
    
    print("Decodificando de Base64...")
    decoded_data = base64.b64decode(encoded_data)
    print(f"Decodificación completada. Tamaño: {len(decoded_data)} bytes")
    return decoded_data

def decrypt_with_des(encrypted_data, key):
    # Paso 5: Descifrar usando DES
    
    print("Iniciando descifrado DES...")
    
    # Crear objeto DES con la misma clave
    des_cipher = pyDes.des(key, pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    
    # Descifrar los datos
    decrypted_data = des_cipher.decrypt(encrypted_data)
    print(f"Descifrado completado. Tamaño: {len(decrypted_data)} bytes")
    
    return decrypted_data

def save_decrypted_image(data, output_path):
    # Paso 6: Guardar la imagen descifrada
    
    print(f"Guardando imagen descifrada: {output_path}")
    
    with open(output_path, 'wb') as file:
        file.write(data)
    
    print("Imagen guardada exitosamente")

def display_image(image_path):
    # Función auxiliar: Mostrar imagen (opcional)
    
    try:
        img = Image.open(image_path)
        img.show()
        print(f"Imagen mostrada: {image_path}")
    except Exception as e:
        print(f"Error al mostrar imagen: {e}")

def find_image_files(directory=None):
    # Busca todos los archivos de imagen en el directorio especificado
    
    if directory is None:
        directory = os.getcwd()  # Directorio actual
    
    # Extensiones de imagen soportadas (en minúsculas y mayúsculas)
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff', '*.webp', '*.ico',
                       '*.JPG', '*.JPEG', '*.PNG', '*.BMP', '*.GIF', '*.TIFF', '*.WEBP', '*.ICO']
    
    image_files = []
    for extension in image_extensions:
        pattern = os.path.join(directory, extension)
        image_files.extend(glob.glob(pattern, recursive=False))
    
    # Eliminar duplicados convirtiendo a set y luego de vuelta a lista
    # Normalizar las rutas para evitar diferencias por separadores
    unique_files = list(set(os.path.normpath(f) for f in image_files))
    
    # Ordenar alfabéticamente para tener un orden consistente
    unique_files.sort()
    
    return unique_files

def select_image_file():
    # Permite al usuario seleccionar una imagen de las disponibles
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_files = find_image_files(current_dir)
    
    if not image_files:
        print("No se encontraron archivos de imagen en el directorio actual")
        print("Formatos soportados: JPG, JPEG, PNG, BMP, GIF, TIFF, WEBP, ICO")
        
        # Ofrecer crear una imagen de prueba
        print("\n¿Quieres crear una imagen de prueba? (s/n):")
        choice = input("Tu elección: ").strip().lower()
        
        if choice in ['s', 'si', 'y', 'yes']:
            test_image = create_test_image()
            if test_image:
                return test_image
        
        return None
    
    print(f"Se encontraron {len(image_files)} archivo(s) de imagen:")
    print("-" * 50)
    
    for i, image_file in enumerate(image_files, 1):
        filename = os.path.basename(image_file)
        file_size = os.path.getsize(image_file)
        print(f"{i}. {filename} ({file_size} bytes)")
    
    while True:
        try:
            print("\nSelecciona el número de la imagen a cifrar (o 0 para salir):")
            choice = input("Tu elección: ").strip()
            
            if choice == '0':
                return None
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(image_files):
                selected_file = image_files[choice_num - 1]
                print(f"Imagen seleccionada: {os.path.basename(selected_file)}")
                return selected_file
            else:
                print(f"Por favor, ingresa un número entre 1 y {len(image_files)}")
                
        except ValueError:
            print("Por favor, ingresa un número válido")
        except KeyboardInterrupt:
            print("\nOperación cancelada por el usuario")
            return None

def create_test_image():
    # Función para crear una imagen de prueba
    
    print("Creando imagen de prueba...")
    
    try:
        # Crear una imagen simple de 200x200 píxeles
        img = Image.new('RGB', (200, 200), color='lightblue')
        
        # Agregar contenido visual
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        
        # Formas geométricas coloridas
        draw.rectangle([50, 50, 150, 150], fill='red', outline='darkred', width=3)
        draw.ellipse([75, 75, 125, 125], fill='yellow', outline='orange', width=2)
        draw.polygon([(100, 30), (130, 50), (70, 50)], fill='green', outline='darkgreen')
        
        # Texto
        try:
            # Intentar usar una fuente del sistema
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            try:
                font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 16)
            except:
                # Si no encuentra la fuente, usar la por defecto
                font = ImageFont.load_default()
        
        draw.text((70, 170), "DES TEST", fill='black', font=font)
        # Guardar la imagen
        test_filename = 'imagen_test.png'
        img.save(test_filename)
        print(f"Imagen de prueba creada: {test_filename}")
        return test_filename
        
    except Exception as e:
        print(f"Error al crear imagen de prueba: {e}")
        return None

def get_input_image():
    # Determina qué imagen usar (argumento de línea de comandos o selección interactiva)
    
    # Verificar si se pasó una imagen como argumento
    if len(sys.argv) > 1:
        input_image = sys.argv[1]
        # Verificar si el archivo existe
        if os.path.exists(input_image):
            # Verificar si es un archivo de imagen válido
            try:
                with Image.open(input_image) as img:
                    img.verify()  # Verificar que es una imagen válida
                print(f"Usando imagen desde argumento: {input_image}")
                return input_image
            except Exception as e:
                print(f"El archivo '{input_image}' no es una imagen válida: {e}")
                print("Cambiando a modo de selección interactiva...")
        else:
            print(f"El archivo '{input_image}' no existe")
            print("Cambiando a modo de selección interactiva...")
    
    # Si no hay argumento o el argumento no es válido, usar selección interactiva
    return select_image_file()


def main():
    # Función principal que ejecuta todo el proceso
    
    print("INICIANDO PROCESO DE CIFRADO Y DESCIFRADO DE IMAGEN CON DES")
    print("=" * 60)
    
    # Configuración - Obtener imagen de entrada
    input_image = get_input_image()
    
    if input_image is None:
        print("No se seleccionó ninguna imagen. Terminando programa.")
        return
    
    # Generar nombre para imagen descifrada manteniendo la extensión original
    base_name = os.path.splitext(os.path.basename(input_image))[0]
    original_ext = os.path.splitext(input_image)[1]
    output_image = f"{base_name}_descifrada{original_ext}"
    
    des_key = b"AC6DF782"  # 8 caracteres = 8 bytes
    print(f"Clave DES: {des_key}")
    print(f"Archivo de entrada: {input_image}")
    print(f"Archivo de salida: {output_image}")
    
    try:
        # PROCESO DE CIFRADO
        print("\n" + "="*30 + " CIFRADO " + "="*30)
        
        # Paso 1: Leer imagen y convertir a bits
        image_data = image_to_bits(input_image)
        
        # Paso 2: Cifrar con DES
        encrypted_data = encrypt_with_des(image_data, des_key)
        
        # Paso 3: Codificar en Base64
        base64_encoded = encode_base64(encrypted_data)
        
        # Paso 4: Mostrar en consola el texto Base64
        print("\n📋 TEXTO CIFRADO EN BASE64:")
        print("-" * 50)
        base64_string = base64_encoded.decode('utf-8')
        
        # Mostrar solo los primeros 400 caracteres para no saturar la consola
        if len(base64_string) > 400:
            print(f"{base64_string[:400]}...")
            print(f"[Mostrando solo los primeros 400 caracteres de {len(base64_string)} totales]")
        else:
            print(base64_string)
        
        # PROCESO DE DESCIFRADO
        print("\n" + "="*30 + " DESCIFRADO " + "="*30)
        
        # Paso 5: Decodificar de Base64
        decoded_data = decode_base64(base64_encoded)
        
        # Paso 6: Descifrar con DES
        decrypted_data = decrypt_with_des(decoded_data, des_key)
        
        # Paso 7: Guardar imagen original
        save_decrypted_image(decrypted_data, output_image)
        
        # Verificar que el proceso fue exitoso
        print("\n" + "="*30 + " VERIFICACIÓN " + "="*30)
        original_size = len(image_data)
        decrypted_size = len(decrypted_data)
        
        print(f" Tamaño original: {original_size} bytes")
        print(f" Tamaño descifrado: {decrypted_size} bytes")
        
        if original_size == decrypted_size and image_data == decrypted_data:
            print("¡ÉXITO! La imagen se cifró y descifró correctamente")
            print("Los datos originales y descifrados son idénticos")
        else:
            print(" ERROR: Los datos no coinciden")
        
        # Mostrar imágenes (opcional)
        print(f"\nImagen original: {input_image}")
        print(f"Imagen descifrada guardada como: {output_image}")
        print("Puedes comparar ambas imágenes para verificar que son idénticas")
        
        # Mostrar las imágenes automáticamente
        print("\nMostrando imagen original...")
        display_image(input_image)
        
        print("Mostrando imagen descifrada...")
        display_image(output_image)
        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{input_image}'")
        print("Asegúrate de que 'secret.jpg' esté en el mismo directorio que este programa")
        print("Verifica que el nombre del archivo sea exactamente 'secret.jpg'")
    except Exception as e:
        print(f"Error inesperado: {e}")

# FUNCIÓN PARA MOSTRAR INFORMACIÓN DE USO
def show_usage():
    # Muestra información sobre cómo usar el programa
    
    print("📋 USO DEL PROGRAMA:")
    print("=" * 50)
    print("1. Ejecutar sin argumentos para modo interactivo:")
    print("   python des.py")
    print("")
    print("2. Ejecutar con una imagen específica:")
    print("   python des.py ruta/a/tu/imagen.jpg")
    print("")
    print("📋 FORMATOS SOPORTADOS:")
    print("   JPG, JPEG, PNG, BMP, GIF, TIFF, WEBP, ICO")
    print("")
    print("💡 EJEMPLOS:")
    print("   python des.py secret.jpg")
    print("   python des.py mi_foto.png")
    print("   python des.py C:\\imagenes\\foto.bmp")

if __name__ == "__main__":
    # Verificar si el usuario pidió ayuda
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', '/?']:
        show_usage()
    else:
        main()

