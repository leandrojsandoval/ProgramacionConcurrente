import requests
import json

# URL de la API (modificar con la que desees usar)
url = 'https://api.ejemplo.com/datos'

# Enviar la petición GET a la API
response = requests.get(url)

# Verificar que la petición fue exitosa (código 200)
if response.status_code == 200:
    # Almacenar la respuesta en formato JSON
    datos = response.json()
    
    # Ahora puedes acceder a los valores de 'datos'
    # Ejemplo: supongamos que el JSON tiene una clave 'nombre' y 'edad'
    nombre = datos.get('nombre', 'No disponible')
    edad = datos.get('edad', 'No disponible')
    
    print(f"Nombre: {nombre}")
    print(f"Edad: {edad}")
else:
    print(f"Error al hacer la petición. Código de estado: {response.status_code}")


foto_url = datos.get('foto_url')
    
response_imagen = requests.get(foto_url)
if response_imagen.status_code == 200:
    # Guardar la imagen en un archivo local (ejemplo: 'imagen.jpg')
    with open('imagen.jpg', 'wb') as archivo_imagen:
        archivo_imagen.write(response_imagen.content)
