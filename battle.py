import constants, game_context, selector_character_menu, os, pygame, random, utils
from button import Button

# ===================================== Variables =====================================

# Cargar imágenes de fondo aleatoriamente
bg_images = [
    file for file in os.listdir(constants.NAME_FOLDER_BACKGROUNDS)
    if file.endswith((".png", ".jpg")) and "background" in file
]
bg_image_path = os.path.join(
    constants.NAME_FOLDER_BACKGROUNDS,
    random.choice(bg_images))  # Selecciona una imagen aleatoriamente
bg_image = pygame.image.load(bg_image_path)

# Escalar la imagen de fondo a las dimensiones de la ventana
window = game_context.get_window()
bg_image = pygame.transform.scale(
    bg_image, (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))

# ===================================== Botones =====================================


def create_actions_buttons():
    buttons = []
    button_colors = [
        constants.COLOR_ORANGE_TUPLE,
        constants.COLOR_CYAN_TUPLE,
        constants.COLOR_VIOLET_TUPLE,
        constants.COLOR_GREEN_TUPLE,
    ]
    button_colors_hover = [
        constants.COLOR_LIGHT_ORANGE_TUPLE,
        constants.COLOR_LIGHT_CYAN_TUPLE,
        constants.COLOR_LIGHT_VIOLET_TUPLE,
        constants.COLOR_LIGHT_GREEN_TUPLE,
    ]
    button_font = pygame.font.Font(
        constants.PATH_FONTS + constants.FONT_GAMEPLAY,
        constants.SIZE_FONT_BUTTONS_BATTLE_MENU,
    )
    for i, action in enumerate([
            constants.ATACAR,
            constants.DEFENDER,
            constants.DESCANSAR,
            constants.CONCENTRARSE,
    ]):
        position_x = (constants.WINDOW_WIDTH -
                      (constants.BUTTON_WIDTH * constants.TOTAL_BUTTONS +
                       constants.BUTTONS_SPACING_BATTLE_ACTIONS *
                       (constants.TOTAL_BUTTONS - 1))) // 2 + i * (
                           constants.BUTTON_WIDTH +
                           constants.BUTTONS_SPACING_BATTLE_ACTIONS)
        position_y = constants.WINDOW_HEIGHT - 100
        button_color = button_colors[i]
        button_hover_color = button_colors_hover[i]
        buttons.append(
            Button(
                action,
                position_x,
                position_y,
                constants.BUTTON_WIDTH,
                constants.BUTTON_HEIGHT,
                button_color,
                button_hover_color,
                constants.COLOR_BLACK_TUPLE,
                constants.PIXELS_BORDER_BUTTON,
                button_font,
            ))
    return buttons


# ===================================== Batalla =====================================


def handle_player_action(button, current_character, enemy_character):
    action = button.text
    if action == constants.ATACAR:
        damage = current_character.attack(enemy_character)
        print("===================================================")
        print(
            f"{current_character.name} atacó a {enemy_character.name} causando {damage} de daño."
        )
        print(
            f"{enemy_character.name} ahora tiene {enemy_character.health} HP.")
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
    print(
        f"{enemy_character.name} atacó a {current_character.name} causando {enemy_character.attack_power} de daño."
    )
    print(
        f"{current_character.name} ahora tiene {current_character.health} HP.")
    print("===================================================")


# ===================================== Batalla =====================================


def start_battle(current_character, enemy_character):
    running = True
    turn = constants.PLAYER
    button_actions = create_actions_buttons()

    while running:
        window.blit(bg_image, (0, 0))

        utils.draw_conditions(current_character, enemy_character)

        if current_character.health <= 0 or enemy_character.health <= 0:
            running = False
            continue

        utils.draw_characters(current_character, enemy_character)

        utils.draw_buttons(button_actions)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Salir completamente del juego
                exit()  # Salir del programa
            if event.type == pygame.MOUSEBUTTONDOWN and turn == constants.PLAYER:
                for button in button_actions:
                    if button.is_clicked():
                        turn = handle_player_action(button, current_character,
                                                    enemy_character)
                        break

        if turn == constants.ENEMY:
            handle_enemy_turn(current_character, enemy_character)
            turn = constants.PLAYER

        pygame.display.update()

    # Declarar el ganador
    winner = current_character if current_character.health > 0 else enemy_character
    pygame.display.update()

    # Mostrar mensaje "Presione Enter para continuar"
    waiting_for_enter = True

    title_character_won = f"{winner.name} ha ganado!"

    while waiting_for_enter:
        window.blit(bg_image, (0, 0))

        utils.draw_text(
            title_character_won, constants.FONT_GAMEPLAY,
            constants.SIZE_TITLE_CHARACTER_WON, constants.COLOR_WHITE_TUPLE,
            utils.calculate_centered_x_position(
                title_character_won, constants.FONT_GAMEPLAY,
                constants.SIZE_TITLE_CHARACTER_WON),
            constants.POSITION_Y_TITLE_CHARACTER_WON)

        utils.draw_text(
            constants.MESSAGE_CHARACTER_WON, constants.FONT_GAMEPLAY,
            constants.SIZE_MESSAGE_CHARACTER_WON, constants.COLOR_WHITE_TUPLE,
            utils.calculate_centered_x_position(
                constants.MESSAGE_CHARACTER_WON, constants.FONT_GAMEPLAY,
                constants.SIZE_MESSAGE_CHARACTER_WON),
            constants.POSITION_Y_MESSAGE_CHARACTER_WON)

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting_for_enter = False  # Cuando se presiona Enter, salir del bucle

    # Volver al menú principal, sin cerrar pygame
    selector_character_menu.main_menu()
