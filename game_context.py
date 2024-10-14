import api, archivo, constants, json, os, pygame
from character import Character

# ===================================== Ventana =====================================

window = pygame.display.set_mode(
    (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
pygame.display.set_caption(constants.GAME_NAME)

# ===================================== Personajes =====================================

"""""""""
def load_characters_from_json():
    characters = {}
    sprites = []

    # Verificar si la carpeta de personajes existe
    if not os.path.exists(constants.NAME_FOLDER_CHARACTERS):
        os.makedirs(constants.NAME_FOLDER_CHARACTERS)

    # Descargar personajes
    for character_id in range(1, constants.CANTIDAD_DE_PERSONAJES + 1):
        api.get_character_by_id(constants.URL_API, character_id,
                                constants.NAME_FOLDER_CHARACTERS)

    # Cargar los archivos JSON existentes
    for archivo in os.listdir(constants.NAME_FOLDER_CHARACTERS):
        if archivo.endswith(".json"):
            with open(f"{constants.NAME_FOLDER_CHARACTERS}/{archivo}",
                      "r") as f:
                character_data = json.load(f)
                name = character_data.get("name", "No disponible")
                health = character_data["stats"][0]["base_stat"]
                attack = character_data["stats"][1]["base_stat"]
                defense = character_data["stats"][2]["base_stat"]
                character = Character(name.capitalize(), health, attack,
                                      defense, sprites)
                print(character.to_string())
                characters[character.name] = character

    return characters
"""

#characters = load_characters_from_json()

characters = archivo.load_characters_from_json(constants.NAME_FOLDER_CHARACTERS)

# ===================================== Sprites =====================================


def load_sprites():
    sprites = {}
    for character in characters.values():
        front_sprite_path = f"sprites/{character.name}_front_default.png"
        back_sprite_path = f"sprites/{character.name}_back_default.png"

        # Si los sprites no existen, se deben descargar
        if not os.path.exists(front_sprite_path) or not os.path.exists(
                back_sprite_path):
            print(f"Descargando sprites para {character.name}...")
            api.download_sprite(character.sprites["front_default"],
                                character.name, "front_default")
            api.download_sprite(character.sprites["back_default"],
                                character.name, "back_default")

        # Cargar los sprites desde el sistema de archivos
        front_sprite = pygame.image.load(front_sprite_path).convert_alpha()
        back_sprite = pygame.image.load(back_sprite_path).convert_alpha()

        sprites[character.name] = {"front": front_sprite, "back": back_sprite}

    return sprites


#sprites = load_sprites()

# ===================================== Gets =====================================


def get_window():
    return window


def get_sprites():
    characters = get_characters()
    sprites = {}

    for c in characters:
        # Cargar los sprites desde el sistema de archivos
        front_sprite_path = c.sprites["front_default"]  # Ruta del sprite frontal
        back_sprite_path = c.sprites["back_default"]    # Ruta del sprite trasero

        # Cargar las imágenes con pygame
        front_sprite = pygame.image.load(front_sprite_path).convert_alpha()
        back_sprite = pygame.image.load(back_sprite_path).convert_alpha()

        # Almacenar las imágenes cargadas en el diccionario
        sprites[c.name] = {
            "front": front_sprite,
            "back": back_sprite
        }

    return sprites

def get_characters():
    return characters
