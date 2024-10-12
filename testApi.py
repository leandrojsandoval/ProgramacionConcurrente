import json
import os
from pokemon import Pokemon

# Función para cargar los archivos JSON de la carpeta 'characters'
def cargar_pokemons():
    pokemons = {}
    
    # Iterar sobre los archivos en la carpeta 'characters'
    for archivo in os.listdir('characters'):
        if archivo.endswith('.json'):
            with open(f'characters/{archivo}', 'r') as f:
                pokemon_data = json.load(f)
                # Crear un objeto Pokemon usando el método from_api
                pokemon = Pokemon.from_api(pokemon_data)
                # Guardar el Pokémon en el diccionario con su nombre como clave
                pokemons[pokemon.name] = pokemon  # Usar el nombre capitalizado como clave

    return pokemons

# Cargar los Pokémon
coleccion_pokemons = cargar_pokemons()

# Mostrar información de los Pokémon cargados
for nombre, pokemon in coleccion_pokemons.items():
    print(f"Nombre: {nombre}, Salud: {pokemon.health}, Ataque: {pokemon.attack_power}, Defensa: {pokemon.defense}, Sprites: {pokemon.sprites}")

# Ejemplo de búsqueda por nombre
nombre_busqueda = 'Bulbasaur'
pokemon_buscado = coleccion_pokemons.get(nombre_busqueda.capitalize())  # Usar capitalize para asegurarse de que coincida
if pokemon_buscado:
    print(f"\nDatos de {nombre_busqueda}:")
    print(f"Nombre: {pokemon_buscado.name}, Salud: {pokemon_buscado.health}, Ataque: {pokemon_buscado.attack_power}, Defensa: {pokemon_buscado.defense}")
    print(f"Sprites: {pokemon_buscado.sprites}")  # Imprime las rutas locales de los sprites
else:
    print(f"{nombre_busqueda} no encontrado.")
