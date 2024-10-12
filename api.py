import requests
import json
import os

# Crear la carpeta 'characters' si no existe
if not os.path.exists('characters'):
    os.makedirs('characters')

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
            'sprites': pokemon_datos.get('sprites', {}).get('versions', {}).get('generation-iii', {}).get('firered-leafgreen', {}),  # Sprites de FR/LG
            'stats': [{
                'stat_name': stat['stat']['name'],
                'base_stat': stat['base_stat']
            } for stat in pokemon_datos.get('stats', [])]  # Las estadísticas del Pokémon
        }

        # Guardar el JSON filtrado en la carpeta 'characters' con el nombre del Pokémon
        nombre_pokemon = pokemon_filtrado['name']
        with open(f'characters/{nombre_pokemon}.json', 'w') as archivo_json:
            json.dump(pokemon_filtrado, archivo_json, indent=4)

        # Mostrar la información filtrada en consola
        print(f"Nombre: {pokemon_filtrado['name']}")
        print("Sprites:")
        for key, value in pokemon_filtrado['sprites'].items():
            print(f"  {key}: {value}")

        print("Stats:")
        for stat in pokemon_filtrado['stats']:
            print(f"  {stat['stat_name']}: {stat['base_stat']}")
    else:
        print(f"Error al hacer la petición para el Pokémon ID {pokemon_id}. Código de estado: {response.status_code}")

# Iterar sobre los primeros 10 Pokémon
for pokemon_id in range(1, 11):
    obtener_pokemon_por_id(pokemon_id)
