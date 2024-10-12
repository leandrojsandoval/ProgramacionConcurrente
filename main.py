import pygame

from pokemon import Pokemon
from boton import Boton

pygame.init()

running = True

# Dimensiones de la ventana
INITIAL_WIDTH = 1024
INITIAL_HEIGHT = 768
WINDOW = pygame.display.set_mode((INITIAL_WIDTH, INITIAL_HEIGHT), pygame.RESIZABLE)  # Modo ventana y resizable
pygame.display.set_caption("Combate por Turnos Estilo Pokémon")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
DARK_GRAY = (105, 105, 105)

# Tamaño de los botones
BUTTON_SPACING = 20     # Espacio entre botones
TOTAL_BUTTONS = 4       # Número total de botones
BUTTON_WIDTH = 150      # Ancho deseado de los botones
ATACAR = "Atacar"
DEFENDER = "Defender"
DESCANSAR = "Descansar"
CONCENTRARSE = "Concentrarse"

def create_buttons():
    buttons = []
    for i, action in enumerate([ATACAR, DEFENDER, DESCANSAR, CONCENTRARSE]):
        x = (INITIAL_WIDTH - (BUTTON_WIDTH * TOTAL_BUTTONS + BUTTON_SPACING * (TOTAL_BUTTONS - 1))) // 2 + i * (BUTTON_WIDTH + BUTTON_SPACING)
        y = INITIAL_HEIGHT - 100
        buttons.append(Boton(action, x, y, BUTTON_WIDTH, 50, (100, 200, 100), (150, 250, 150)))
    return buttons

# Cargar imágenes
ESCALE_FACTOR = 3
bg_image = pygame.image.load('assets/background_bosque.png')
pikachu_image = pygame.image.load('assets/pikachu_espalda.png')
bulbasaur_image = pygame.image.load('assets/bulbasaur_espalda.png')
pikachu_image = pygame.transform.scale(pikachu_image, (int(pikachu_image.get_width() * ESCALE_FACTOR), int(pikachu_image.get_height() * ESCALE_FACTOR)))
bulbasaur_image = pygame.transform.scale(bulbasaur_image, (int(bulbasaur_image.get_width() * ESCALE_FACTOR), int(bulbasaur_image.get_height() * ESCALE_FACTOR)))

# Crear personajes
PIKACHU = "Pikachu"
BULBASAUR = "Bulbasaur"
pikachu = Pokemon(PIKACHU, 100, 20, 10)
bulbasaur = Pokemon(BULBASAUR, 100, 15, 50)
pokemons = [pikachu, bulbasaur]
current_selection = 0

def load_list_characters():

    for i, pokemon in enumerate(pokemons):
        
        draw_text(pokemon.name, 40, 250, 200 + i * 100)
        
        if current_selection == i:
            pygame.draw.rect(WINDOW, BLACK, (240, 190 + i * 100, 300, 50), 2)
            image_to_draw = pikachu_image if pokemon.name == PIKACHU else bulbasaur_image
            WINDOW.blit(image_to_draw, (500, 200))

# Auxiliares
ENEMY = "Enemy"
PLAYER = "Player"
def draw_text(text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, BLACK)
    WINDOW.blit(text_surface, (x, y))

# Vista Menu Principal
def handle_events():

    global current_selection

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            return None
        
        if event.type == pygame.KEYDOWN:

            if event.key in (pygame.K_DOWN, pygame.K_UP):
                direction = 1 if event.key == pygame.K_DOWN else -1
                current_selection = (current_selection + direction) % len(pokemons)
            elif event.key == pygame.K_RETURN:
                return pokemons[current_selection]

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            for i, pokemon in enumerate(pokemons):
                if 250 <= mouse_x <= 550 and (200 + i * 100) <= mouse_y < (250 + i * 100):
                    return pokemons[i]

    return None

def main_menu():

    global running

    while running:

        WINDOW.fill(WHITE)
        WINDOW.blit(bg_image, (0, 0))

        draw_text("Elige tu Pokémon", 60, 250, 50)

        load_list_characters()

        selected_pokemon = handle_events()
        if selected_pokemon is not None:
            return selected_pokemon
        
        pygame.display.update()

# Vista Batalla
def draw_conditions(current_pokemon, enemy_pokemon):
    draw_text(f"{current_pokemon.name} HP: {current_pokemon.health}", 40, 50, 50)
    draw_text(f"{enemy_pokemon.name} HP: {enemy_pokemon.health}", 40, 50, 100)

def draw_pokemons(current_pokemon, enemy_pokemon):
    current_pokemon_x = INITIAL_WIDTH // 2
    enemy_pokemon_x = INITIAL_WIDTH // 2
    enemy_pokemon_size = (int(bulbasaur_image.get_width() * 1.5), int(bulbasaur_image.get_height() * 1.5))

    if current_pokemon.name == PIKACHU:
        WINDOW.blit(pikachu_image, (current_pokemon_x, INITIAL_HEIGHT - 200))
        WINDOW.blit(pygame.transform.scale(bulbasaur_image, enemy_pokemon_size), (enemy_pokemon_x, INITIAL_HEIGHT - 600))
    else:
        WINDOW.blit(pygame.transform.scale(bulbasaur_image, enemy_pokemon_size), (enemy_pokemon_x, INITIAL_HEIGHT - 400))
        WINDOW.blit(pikachu_image, (current_pokemon_x, INITIAL_HEIGHT - 200))

def handle_player_action(button, current_pokemon, enemy_pokemon):
    action = button.text
    if action == ATACAR:
        damage = current_pokemon.attack(enemy_pokemon)
        print("===================================================")
        print(f"{current_pokemon.name} atacó a {enemy_pokemon.name} causando {damage} de daño.")
        print(f"{enemy_pokemon.name} ahora tiene {enemy_pokemon.health} HP.")
        print("===================================================")
        return ENEMY
    elif action == DEFENDER:
        print("===================================================")
        current_pokemon.defend()
        print(f"{current_pokemon.name} se está defendiendo.")
        print("===================================================")
        return ENEMY
    elif action == DESCANSAR:
        print("===================================================")
        current_pokemon.rest()
        print(f"{current_pokemon.name} descansó y recuperó salud.")
        print("===================================================")
        return ENEMY
    elif action == CONCENTRARSE:
        print("===================================================")
        current_pokemon.focus()
        print(f"{current_pokemon.name} está concentrando su ataque.")
        print("===================================================")
        return ENEMY
    return PLAYER

def handle_enemy_turn(current_pokemon, enemy_pokemon):
    damage = enemy_pokemon.attack(current_pokemon)
    print(f"{enemy_pokemon.name} atacó a {current_pokemon.name} causando {enemy_pokemon.attack_power} de daño.")
    print(f"{current_pokemon.name} ahora tiene {current_pokemon.health} HP.")
    print("===================================================")

def draw_buttons(buttons, mouse_pos):
    global WINDOW
    for button in buttons:
        button.draw(WINDOW, mouse_pos)

def battle(current_pokemon, enemy_pokemon):
    global running
    turn = PLAYER
    button_actions = create_buttons()

    while running:
        WINDOW.blit(bg_image, (0, 0))

        draw_conditions(current_pokemon, enemy_pokemon)

        if current_pokemon.health <= 0 or enemy_pokemon.health <= 0:
            running = False
            continue

        draw_pokemons(current_pokemon, enemy_pokemon)

        mouse_pos = pygame.mouse.get_pos()
        draw_buttons(button_actions, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and turn == PLAYER:
                mouse_pos = event.pos
                for button in button_actions:
                    if button.is_clicked(mouse_pos):
                        turn = handle_player_action(button, current_pokemon, enemy_pokemon)
                        break

        if turn == ENEMY:
            handle_enemy_turn(current_pokemon, enemy_pokemon)
            turn = PLAYER

        pygame.display.update()

    winner = current_pokemon if current_pokemon.health > 0 else enemy_pokemon
    draw_text(f"{winner.name} ha ganado!", 60, 250, 250)
    pygame.display.update()
    pygame.time.delay(2000)

if __name__ == "__main__":
    selected_pokemon = main_menu()
    enemy_pokemon = bulbasaur if selected_pokemon == pikachu else pikachu
    battle(selected_pokemon, enemy_pokemon)
    pygame.quit()
