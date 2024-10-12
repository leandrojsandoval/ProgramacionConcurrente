import constants, json, os, pygame 
from pokemon import Pokemon

#===================================== Ventana =====================================

window = pygame.display.set_mode((constants.INITIAL_WIDTH, constants.INITIAL_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption(constants.GAME_NAME)

#===================================== Personajes =====================================

def load_characters_from_json():
    characters = {}

    for archivo in os.listdir('characters'):
        if archivo.endswith('.json'):
            with open(f'characters/{archivo}', 'r') as f:
                character_data = json.load(f)
                character = Pokemon.from_json(character_data)
                characters[character.name] = character
    return characters

characters = load_characters_from_json()

#===================================== Sprites =====================================

def load_sprites():
    sprites = {}
    for pokemon in characters.values():
        front_sprite = pygame.image.load(pokemon.sprites['front_default']).convert_alpha()
        back_sprite = pygame.image.load(pokemon.sprites['back_default']).convert_alpha()
        sprites[pokemon.name] = {
            'front': front_sprite,
            'back': back_sprite
        }
    return sprites

sprites = load_sprites()

#===================================== Gets =====================================

def get_window():
    return window

def get_sprites():
    return sprites

def get_characters():
    return characters
