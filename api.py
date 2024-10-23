import constants
import json
import os
import requests


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
        if response.status_code == constants.HTTP_OK:
            with open(sprite_path, "wb") as file:
                file.write(response.content)
        else:
            print(f"Error al descargar el sprite de {character_name} ({type_sprite}): Código de estado {response.status_code}")
    else:
        print(f"Sprite {type_sprite} de {character_name} ya existe en {sprite_path}.")


def download_and_save_character_data(character_count, api_url, path_folder_characters):
    # Verificar si la carpeta existe, si no, crearla
    if not os.path.exists(path_folder_characters):
        os.makedirs(path_folder_characters)

    for character_id in range(1, character_count + 1):
        full_url = f"{api_url}/{character_id}"
        response = requests.get(full_url)

        if response.status_code == constants.HTTP_OK:
            response_data = response.json()

            character_data = {
                "name": response_data.get("name", "No disponible").capitalize(),
                "sprites": {
                    "front_default": response_data.get("sprites", {}).get("front_default"),
                    "back_default": response_data.get("sprites", {}).get("back_default"),
                },
                "stats": [
                    {"stat_name": stat["stat"]["name"], "base_stat": stat["base_stat"]}
                    for stat in response_data.get("stats", [])
                ],  # Estadísticas del personaje
            }

            character_name = character_data["name"]

            # Descargar sprites
            for type_sprite, url_sprite in character_data["sprites"].items():
                # Solo descargar si la URL es válida
                if url_sprite:
                    download_sprite(url_sprite, character_name, type_sprite)

            # Extraer los datos relevantes para las estadísticas
            hp = (character_data["stats"][0]["base_stat"]
                  if len(character_data["stats"]) > 0
                  else 0)
            
            attack = (character_data["stats"][1]["base_stat"]
                      if len(character_data["stats"]) > 1
                      else 0)
            
            defense = (character_data["stats"][2]["base_stat"]
                       if len(character_data["stats"]) > 2
                       else 0)

            # Crear un diccionario con los datos que queremos guardar
            character_stats = {
                "name": character_name,
                "hp": hp,
                "attack": attack,
                "defense": defense,
                "front_sprite_path": f"sprites/{character_name.lower()}_front_default.png",
                "back_sprite_path": f"sprites/{character_name.lower()}_back_default.png",
            }

            # Guardar los datos en un archivo JSON
            output_file = os.path.join(path_folder_characters, f"{character_name.capitalize()}{constants.EXTENSION_JSON}")
            
            with open(output_file, "w") as f:
                json.dump(character_stats, f, indent=4)

        else:
            print(f"Error al hacer la petición para el Personaje ID {character_id}. Código de estado: {response.status_code}")
