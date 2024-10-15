import constants, json, os
from character import Character


def load_characters_from_json(output_folder):
    characters = []

    # Listar todos los archivos JSON en la carpeta de salida
    for filename in os.listdir(output_folder):
        if filename.endswith(constants.EXTENSION_JSON):
            file_path = os.path.join(output_folder, filename)

            # Leer el archivo JSON
            with open(file_path, "r") as file:
                character_data = json.load(file)

                # Extraer la información necesaria
                name = character_data["name"]
                hp = character_data["hp"]
                attack = character_data["attack"]
                defense = character_data["defense"]
                front_sprite_path = character_data["front_sprite_path"]
                back_sprite_path = character_data["back_sprite_path"]

                # Crear una lista de sprites
                sprites = {
                    "front_default": front_sprite_path,
                    "back_default": back_sprite_path
                }

                # Instanciar el objeto Character
                character = Character(name, hp, attack, defense, sprites)

                # Agregar el objeto a la lista
                characters.append(character)

    return characters
