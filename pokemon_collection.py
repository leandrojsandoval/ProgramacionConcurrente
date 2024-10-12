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
