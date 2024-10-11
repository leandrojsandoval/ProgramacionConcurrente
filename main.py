# main.py
import pygame
import requests
from pokemon import Pokemon

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 1024, 612
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Combate Pokémon")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
DARK_GRAY = (105, 105, 105)

# Cargar imágenes
bg_image = pygame.image.load('assets/background_bosque.png')  # Asegúrate de tener una imagen de fondo
pikachu_image = pygame.image.load('assets/pikachu_espalda.png')  # Imagen de Pikachu
bulbasaur_image = pygame.image.load('assets/bulbasaur_espalda.png')  # Imagen de Bulbasaur
scale_factor = 3
pikachu_image = pygame.transform.scale(pikachu_image, (int(pikachu_image.get_width() * scale_factor), int(pikachu_image.get_height() * scale_factor)))
bulbasaur_image = pygame.transform.scale(bulbasaur_image, (int(bulbasaur_image.get_width() * scale_factor), int(bulbasaur_image.get_height() * scale_factor)))

# Crear Pokémon
pikachu = Pokemon("Pikachu", 100, 20, 10)
bulbasaur = Pokemon("Bulbasaur", 100, 15, 50)

pokemons = [pikachu, bulbasaur]
current_selection = 0

# Función para mostrar el texto
def draw_text(text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, BLACK)
    WINDOW.blit(text_surface, (x, y))

# Función para el menú principal
def main_menu():
    global current_selection
    running = True
    while running:
        WINDOW.fill(WHITE)
        WINDOW.blit(bg_image, (0, 0))
        draw_text("Elige tu Pokémon", 60, 250, 50)

        # Mostrar Pokémon
        for i, pokemon in enumerate(pokemons):
            draw_text(pokemon.name, 40, 250, 200 + i * 100)
            if current_selection == i:
                pygame.draw.rect(WINDOW, BLACK, (240, 190 + i * 100, 300, 50), 2)
                if pokemon.name == "Pikachu":
                    WINDOW.blit(pikachu_image, (500, 200))
                else:
                    WINDOW.blit(bulbasaur_image, (500, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    current_selection = (current_selection + 1) % len(pokemons)
                elif event.key == pygame.K_UP:
                    current_selection = (current_selection - 1) % len(pokemons)
                elif event.key == pygame.K_RETURN:
                    return pokemons[current_selection]  # Devolver el Pokémon seleccionado

            # Manejo de clics del mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for i, pokemon in enumerate(pokemons):
                    if 250 <= mouse_x <= 550 and (200 + i * 100) <= mouse_y <= (250 + i * 100):
                        return pokemons[i]  # Devolver el Pokémon seleccionado

        pygame.display.update()

# Función para dibujar los botones
def draw_button(text, rect, mouse_pos):
    # Cambiar el color si el mouse está sobre el botón
    color = DARK_GRAY if rect.collidepoint(mouse_pos) else GRAY
    pygame.draw.rect(WINDOW, color, rect)
    draw_text(text, 40, rect.x + 20, rect.y + 10)

# Función principal del juego
def battle(current_pokemon, enemy_pokemon):
    turn = 'player'
    running = True
    button_actions = ['Atacar', 'Defender', 'Descansar', 'Concentrarse']
    button_rects = []
    button_width = WIDTH // len(button_actions)
    button_height = 60

    # Crear los rectángulos para los botones
    for i in range(len(button_actions)):
        button_rects.append(pygame.Rect(i * button_width, HEIGHT - button_height, button_width, button_height))

    while running:
        WINDOW.fill(WHITE)
        WINDOW.blit(bg_image, (0, 0))

        # Mostrar información de los Pokémon
        draw_text(f"{current_pokemon.name} HP: {current_pokemon.health}", 40, 50, 50)
        draw_text(f"{enemy_pokemon.name} HP: {enemy_pokemon.health}", 40, 50, 100)

        # Comprobar si alguno de los Pokémon ha sido derrotado
        if current_pokemon.health <= 0 or enemy_pokemon.health <= 0:
            running = False

        # Dibujar Pokémon
        current_pokemon_x = WIDTH // 2
        enemy_pokemon_x = WIDTH // 2
        enemy_pokemon_size = (int(bulbasaur_image.get_width() * 1.5), int(bulbasaur_image.get_height() * 1.5))

        if current_pokemon.name == "Pikachu":
            WINDOW.blit(pikachu_image, (current_pokemon_x, HEIGHT - 200))
            WINDOW.blit(pygame.transform.scale(bulbasaur_image, enemy_pokemon_size), (enemy_pokemon_x, HEIGHT - 600))
        else:
            WINDOW.blit(pygame.transform.scale(bulbasaur_image, enemy_pokemon_size), (enemy_pokemon_x, HEIGHT - 400))
            WINDOW.blit(pikachu_image, (current_pokemon_x, HEIGHT - 200))

        mouse_pos = pygame.mouse.get_pos()

        # Dibujar los botones
        for i, rect in enumerate(button_rects):
            draw_button(button_actions[i], rect, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(mouse_pos) and turn == 'player':
                        action = button_actions[i]
                        if action == 'Atacar':
                            damage = current_pokemon.attack(enemy_pokemon)
                            print(f"{current_pokemon.name} atacó a {enemy_pokemon.name} causando {current_pokemon.attack_power} de daño.")
                            print(f"{enemy_pokemon.name} ahora tiene {damage} HP.")
                            turn = 'enemy'
                        elif action == 'Defender':
                            current_pokemon.defend()
                            print(f"{current_pokemon.name} se está defendiendo.")
                            turn = 'enemy'
                        elif action == 'Descansar':
                            current_pokemon.rest()
                            print(f"{current_pokemon.name} descansó y recuperó salud.")
                            turn = 'enemy'
                        elif action == 'Concentrarse':
                            current_pokemon.focus()
                            print(f"{current_pokemon.name} está concentrando su ataque.")
                            turn = 'enemy'

                # Turno del enemigo
                if turn == 'enemy':
                    damage = enemy_pokemon.attack(current_pokemon)
                    print(f"{enemy_pokemon.name} atacó a {current_pokemon.name} causando {enemy_pokemon.attack_power} de daño.")
                    print(f"{current_pokemon.name} ahora tiene {damage} HP.")
                    turn = 'player'

        pygame.display.update()

    # Mostrar ganador
    if current_pokemon.health > 0:
        draw_text(f"{current_pokemon.name} ha ganado!", 60, 250, 250)
    else:
        draw_text(f"{enemy_pokemon.name} ha ganado!", 60, 250, 250)

    pygame.display.update()
    pygame.time.wait(2000)

if __name__ == "__main__":
    selected_pokemon = main_menu()
    enemy_pokemon = bulbasaur if selected_pokemon == pikachu else pikachu
    battle(selected_pokemon, enemy_pokemon)
    pygame.quit()
