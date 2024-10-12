import json, os, requests

if not os.path.exists('characters'):
    os.makedirs('characters')
if not os.path.exists('sprites'):
    os.makedirs('sprites')

def download_sprite(url, character_name, type_sprite):
    response = requests.get(url)
    if response.status_code == 200:
        with open(f'sprites/{character_name}_{type_sprite}.png', 'wb') as file:
            file.write(response.content)
    else:
        print(f"Error al descargar el sprite de {character_name} ({type_sprite}): Código de estado {response.status_code}")

def get_character_by_id(character_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{character_id}"

    response = requests.get(url)

    if response.status_code == 200:
        response_data = response.json()

        character_data = {
            'name': response_data.get('name', 'No disponible').capitalize(),
            'sprites': {
                'front_default': response_data.get('sprites', {}).get('front_default'),
                'back_default': response_data.get('sprites', {}).get('back_default')
            },
            'stats': [{
                'stat_name': stat['stat']['name'],
                'base_stat': stat['base_stat']
            } for stat in response_data.get('stats', [])]  # Las estadísticas del Pokémon
        }

        character_name = character_data['name']
        with open(f'characters/{character_name}.json', 'w') as archivo_json:
            json.dump(character_data, archivo_json, indent=4)

        for type_sprite, url in character_data['sprites'].items():
            download_sprite(url, character_name, type_sprite)

    else:
        print(f"Error al hacer la petición para el Personaje ID {character_id}. Código de estado: {response.status_code}")

for character_id in range(1, 11):
    get_character_by_id(character_id)
