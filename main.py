import pygame
import random
import battle
import pokemon_collection
from game_context_singleton import Singleton

pygame.init()

window = Singleton().window

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
DARK_GRAY = (105, 105, 105)

# Cargar imágenes
bg_image = pygame.image.load('assets/background_bosque.png')

# Crear personajes
current_selection = 0
pokemons = pokemon_collection.cargar_pokemons()

def load_list_characters(sprites):
    for i, pokemon in enumerate(pokemons.values()):
        draw_text(pokemon.name, 40, 250, 200 + i * 100)
        
        if current_selection == i:
            pygame.draw.rect(window, BLACK, (240, 190 + i * 100, 300, 50), 2)
            
            # Utiliza el sprite ya cargado
            try:
                image_to_draw = sprites[pokemon.name]['front']  # Usa el sprite ya cargado
                window.blit(image_to_draw, (500, 200))
            except KeyError:
                print(f"Error: El Pokémon {pokemon.name} no tiene sprite cargado.")
            except Exception as e:
                print(f"Error al dibujar la imagen: {e}")

def load_sprites():
    sprites = {}
    for pokemon in pokemons.values():  # Suponiendo que `pokemons` tiene los nombres de los Pokémon como claves
        front_sprite = pygame.image.load(pokemon.sprites['front_default']).convert_alpha()
        back_sprite = pygame.image.load(pokemon.sprites['back_default']).convert_alpha()
        sprites[pokemon.name] = {
            'front': front_sprite,
            'back': back_sprite
        }
    return sprites

# Auxiliares
def draw_text(text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, BLACK)
    window.blit(text_surface, (x, y))

# Vista Menu Principal
def handle_events():
    global current_selection

    # Obtener las claves del diccionario en una lista
    pokemon_names = list(pokemons.keys())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return None
        
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_UP):
                direction = 1 if event.key == pygame.K_DOWN else -1
                current_selection = (current_selection + direction) % len(pokemon_names)
            elif event.key == pygame.K_RETURN:
                # Devuelve el Pokémon correspondiente al nombre seleccionado
                selected_name = pokemon_names[current_selection]
                return pokemons[selected_name]

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            for i, name in enumerate(pokemon_names):
                # Verificar si el mouse está sobre el área del Pokémon
                if 250 <= mouse_x <= 550 and (200 + i * 100) <= mouse_y < (250 + i * 100):
                    return pokemons[name]  # Devuelve el Pokémon correspondiente al nombre

    return None

def main_menu():

    running = True

    while running:

        window.fill(WHITE)
        window.blit(bg_image, (0, 0))

        draw_text("Elige tu Pokémon", 60, 250, 50)

        load_list_characters(sprites)

        selected_pokemon = handle_events()
        if selected_pokemon is not None:
            return selected_pokemon
        
        pygame.display.update()

if __name__ == "__main__":

    sprites = load_sprites()        # Cargar todos los sprites al inicio del programa

    selected_pokemon = main_menu()  # El Pokémon seleccionado por el jugador
    
    if selected_pokemon:
        # Obtén una lista de los Pokémon del mapa (sin incluir el Pokémon seleccionado)
        available_pokemons = [pokemon for name, pokemon in pokemons.items() if pokemon != selected_pokemon]
        
        # Selecciona un Pokémon enemigo al azar de la lista disponible
        enemy_pokemon = random.choice(available_pokemons) if available_pokemons else None

        # Comienza la batalla
        if enemy_pokemon:
            battle.start_battle(selected_pokemon, enemy_pokemon, bg_image, sprites)
        else:
            print("No hay Pokémon enemigos disponibles para la batalla.")
    else:
        print("No se seleccionó ningún Pokémon.")
    
    pygame.quit()
