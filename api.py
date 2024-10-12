import requests
import json
import os

# Crear las carpetas 'characters' y 'sprites' si no existen
if not os.path.exists('characters'):
    os.makedirs('characters')
if not os.path.exists('sprites'):
    os.makedirs('sprites')

# Función para descargar imágenes de los sprites
def descargar_sprite(url, nombre_pokemon, tipo_sprite):
    response = requests.get(url)
    if response.status_code == 200:
        with open(f'sprites/{nombre_pokemon}_{tipo_sprite}.png', 'wb') as file:
            file.write(response.content)
    else:
        print(f"Error al descargar el sprite de {nombre_pokemon} ({tipo_sprite}): Código de estado {response.status_code}")

# Función para obtener y guardar información de un Pokémon dado su ID
def obtener_pokemon_por_id(pokemon_id):
    # URL de la API de PokeAPI para obtener información del Pokémon por ID
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"

    # Enviar la petición GET a la API
    response = requests.get(url)

    # Verificar que la petición fue exitosa (código 200)
    if response.status_code == 200:
        # Almacenar la respuesta en formato JSON
        pokemon_datos = response.json()

        # Seleccionar solo 'name', 'sprites' y 'stats' del JSON
        pokemon_filtrado = {
            'name': pokemon_datos.get('name', 'No disponible'),
            'sprites': {
                'front_default': pokemon_datos.get('sprites', {}).get('front_default'),
                'back_default': pokemon_datos.get('sprites', {}).get('back_default')
            },
            'stats': [{
                'stat_name': stat['stat']['name'],
                'base_stat': stat['base_stat']
            } for stat in pokemon_datos.get('stats', [])]  # Las estadísticas del Pokémon
        }

        # Guardar el JSON filtrado en la carpeta 'characters' con el nombre del Pokémon
        nombre_pokemon = pokemon_filtrado['name']
        with open(f'characters/{nombre_pokemon}.json', 'w') as archivo_json:
            json.dump(pokemon_filtrado, archivo_json, indent=4)

        # Descargar los sprites
        for tipo_sprite, url in pokemon_filtrado['sprites'].items():
            descargar_sprite(url, nombre_pokemon, tipo_sprite)

        # Mostrar la información filtrada en consola
        print(f"Nombre: {pokemon_filtrado['name']}")
        print("Sprites descargados:")
        for tipo_sprite in pokemon_filtrado['sprites']:
            print(f"  {tipo_sprite}: sprites/{nombre_pokemon}_{tipo_sprite}.png")

        print("Stats:")
        for stat in pokemon_filtrado['stats']:
            print(f"  {stat['stat_name']}: {stat['base_stat']}")
    else:
        print(f"Error al hacer la petición para el Pokémon ID {pokemon_id}. Código de estado: {response.status_code}")

# Iterar sobre los primeros 10 Pokémon
for pokemon_id in range(1, 11):
    obtener_pokemon_por_id(pokemon_id)
