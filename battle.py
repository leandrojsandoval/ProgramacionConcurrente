import pygame
from boton import Boton
from main import draw_text
from game_context_singleton import Singleton
import constants

#===================================== Constantes =====================================



ATACAR = "Atacar"
DEFENDER = "Defender"
DESCANSAR = "Descansar"
CONCENTRARSE = "Concentrarse"

ENEMY = "Enemy"
PLAYER = "Player"

#===================================== Variables =====================================

window = Singleton().window

#===================================== Botones =====================================

def create_buttons():
    buttons = []
    for i, action in enumerate([ATACAR, DEFENDER, DESCANSAR, CONCENTRARSE]):

        x = (constants.INITIAL_WIDTH - (constants.BUTTON_WIDTH * constants.TOTAL_BUTTONS + constants.BUTTON_SPACING * (constants.TOTAL_BUTTONS - 1))) // 2 + i * (constants.BUTTON_WIDTH + constants.BUTTON_SPACING)
        y = constants.INITIAL_HEIGHT - 100
        buttons.append(Boton(action, x, y, constants.BUTTON_WIDTH, 50, (100, 200, 100), (150, 250, 150)))
    return buttons

#===================================== Dibujo =====================================

def draw_conditions(current_pokemon, enemy_pokemon):
    draw_text(f"{current_pokemon.name} HP: {current_pokemon.health}", 40, 50, 50)
    draw_text(f"{enemy_pokemon.name} HP: {enemy_pokemon.health}", 40, 50, 100)

def draw_buttons(buttons, mouse_pos):
    for button in buttons:
        button.draw(window, mouse_pos)

def draw_pokemons(current_pokemon, enemy_pokemon, sprites):
    current_pokemon_x = constants.INITIAL_WIDTH // 2
    enemy_pokemon_x = constants.INITIAL_WIDTH // 2
    enemy_pokemon_size = (int(sprites[enemy_pokemon.name]['front'].get_width() * 1.5), int(sprites[enemy_pokemon.name]['front'].get_height() * 1.5))

    window.blit(sprites[current_pokemon.name]['back'], (current_pokemon_x, constants.INITIAL_HEIGHT - 200))

    window.blit(pygame.transform.scale(sprites[enemy_pokemon.name]['front'], enemy_pokemon_size), (enemy_pokemon_x, constants.INITIAL_HEIGHT - 600))

#===================================== Batalla =====================================

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

def start_battle(current_pokemon, enemy_pokemon, bg_image, sprites):
    running = True
    turn = PLAYER
    button_actions = create_buttons()

    while running:
        window.blit(bg_image, (0, 0))

        draw_conditions(current_pokemon, enemy_pokemon)

        if current_pokemon.health <= 0 or enemy_pokemon.health <= 0:
            running = False
            continue

        draw_pokemons(current_pokemon, enemy_pokemon, sprites)

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
