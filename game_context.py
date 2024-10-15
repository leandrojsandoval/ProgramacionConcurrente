import api, archivo, constants, os, pygame

# ===================================== Ventana =====================================

window = pygame.display.set_mode(
    (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
pygame.display.set_caption(constants.GAME_NAME)

# ===================================== Personajes =====================================

# Uso de la función
if not os.path.exists(constants.PATH_CHARACTERS) or not os.path.exists(constants.PATH_SPRITES):
    api.download_and_save_character_data(constants.NUMBER_OF_CHARACTERS,
                                         constants.URL_API,
                                         constants.PATH_CHARACTERS)
characters = archivo.load_characters_from_json(constants.PATH_CHARACTERS)

# ===================================== Gets =====================================


def get_window():
    return window


def get_sprites():
    characters = get_characters()
    sprites = {}

    for character in characters:
        # Cargar los sprites desde el sistema de archivos
        front_sprite_path = character.sprites[
            "front_default"]  # Ruta del sprite frontal
        back_sprite_path = character.sprites[
            "back_default"]  # Ruta del sprite trasero

        # Cargar las imágenes con pygame
        front_sprite = pygame.image.load(front_sprite_path).convert_alpha()
        back_sprite = pygame.image.load(back_sprite_path).convert_alpha()

        # Almacenar las imágenes cargadas en el diccionario
        sprites[character.name] = {"front": front_sprite, "back": back_sprite}

    return sprites


def get_characters():
    return characters
