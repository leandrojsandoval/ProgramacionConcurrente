import json, os, requests


def get_character_by_id(url, character_id, path_folder_characters):
    full_url = f"{url}/{character_id}"

    response = requests.get(full_url)

    if response.status_code == 200:
        response_data = response.json()

        character_data = {
            "name": response_data.get("name", "No disponible").capitalize(),
            "sprites": {
                "front_default": response_data.get("sprites",
                                                   {}).get("front_default"),
                "back_default": response_data.get("sprites",
                                                  {}).get("back_default"),
            },
            "stats": [{
                "stat_name": stat["stat"]["name"],
                "base_stat": stat["base_stat"]
            } for stat in response_data.get("stats", [])
                     ],  # Las estadísticas del Pokémon
        }

        character_name = character_data["name"]
        character_file = f"{path_folder_characters}/{character_name}.json"

        # Solo guardar el archivo JSON si no existe
        if not os.path.exists(character_file):
            with open(character_file, "w") as archivo_json:
                json.dump(character_data, archivo_json, indent=4)

        # Descargar sprites
        for type_sprite, url_sprite in character_data["sprites"].items():
            download_sprite(url_sprite, character_name, type_sprite)

    else:
        print(
            f"Error al hacer la petición para el Personaje ID {character_id}. Código de estado: {response.status_code}"
        )


def download_sprite(url, character_name, type_sprite):
    sprite_folder = "sprites"
    sprite_path = f"{sprite_folder}/{character_name}_{type_sprite}.png"

    # Crear la carpeta 'sprites' si no existe
    if not os.path.exists(sprite_folder):
        try:
            os.makedirs(sprite_folder)
        except OSError as e:
            print(f"Error al crear la carpeta '{sprite_folder}': {e}")
            return

    if not url:
        print(f"No hay URL disponible para {character_name} ({type_sprite}).")
        return

    # Solo descargar el sprite si no existe
    if not os.path.exists(sprite_path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(sprite_path, "wb") as file:
                file.write(response.content)
        else:
            print(
                f"Error al descargar el sprite de {character_name} ({type_sprite}): Código de estado {response.status_code}"
            )
