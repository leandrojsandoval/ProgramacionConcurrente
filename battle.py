import constants, game_context, pygame, utils
from boton import Boton

#===================================== Variables =====================================

window = game_context.get_window()

#===================================== Botones =====================================

def create_buttons():
    buttons = []
    for i, action in enumerate([constants.ATACAR, constants.DEFENDER, constants.DESCANSAR, constants.CONCENTRARSE]):

        x = (constants.INITIAL_WIDTH - (constants.BUTTON_WIDTH * constants.TOTAL_BUTTONS + constants.BUTTON_SPACING * (constants.TOTAL_BUTTONS - 1))) // 2 + i * (constants.BUTTON_WIDTH + constants.BUTTON_SPACING)
        y = constants.INITIAL_HEIGHT - 100
        buttons.append(Boton(action, x, y, constants.BUTTON_WIDTH, 50, (100, 200, 100), (150, 250, 150)))
    return buttons

#===================================== Batalla =====================================

def handle_player_action(button, current_character, enemy_character):
    action = button.text
    if action == constants.ATACAR:
        damage = current_character.attack(enemy_character)
        print("===================================================")
        print(f"{current_character.name} atacó a {enemy_character.name} causando {damage} de daño.")
        print(f"{enemy_character.name} ahora tiene {enemy_character.health} HP.")
        print("===================================================")
        return constants.ENEMY
    elif action == constants.DEFENDER:
        print("===================================================")
        current_character.defend()
        print(f"{current_character.name} se está defendiendo.")
        print("===================================================")
        return constants.ENEMY
    elif action == constants.DESCANSAR:
        print("===================================================")
        current_character.rest()
        print(f"{current_character.name} descansó y recuperó salud.")
        print("===================================================")
        return constants.ENEMY
    elif action == constants.CONCENTRARSE:
        print("===================================================")
        current_character.focus()
        print(f"{current_character.name} está concentrando su ataque.")
        print("===================================================")
        return constants.ENEMY
    return constants.PLAYER

def handle_enemy_turn(current_character, enemy_character):
    damage = enemy_character.attack(current_character)
    print(f"{enemy_character.name} atacó a {current_character.name} causando {enemy_character.attack_power} de daño.")
    print(f"{current_character.name} ahora tiene {current_character.health} HP.")
    print("===================================================")

def start_battle(current_character, enemy_character, bg_image):
    running = True
    turn = constants.PLAYER
    button_actions = create_buttons()

    while running:
        window.blit(bg_image, (0, 0))

        utils.draw_conditions(current_character, enemy_character)

        if current_character.health <= 0 or enemy_character.health <= 0:
            running = False
            continue

        utils.draw_characters(current_character, enemy_character)

        mouse_pos = pygame.mouse.get_pos()
        utils.draw_buttons(button_actions, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and turn == constants.PLAYER:
                mouse_pos = event.pos
                for button in button_actions:
                    if button.is_clicked(mouse_pos):
                        turn = handle_player_action(button, current_character, enemy_character)
                        break

        if turn == constants.ENEMY:
            handle_enemy_turn(current_character, enemy_character)
            turn = constants.PLAYER

        pygame.display.update()

    winner = current_character if current_character.health > 0 else enemy_character
    utils.draw_text(f"{winner.name} ha ganado!", 60, 250, 250)
    pygame.display.update()
    pygame.time.delay(2000)
