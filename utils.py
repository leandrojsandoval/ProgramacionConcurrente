import constants, game_context, os, pygame

window = game_context.get_window()
sprites = game_context.get_sprites()


def draw_conditions(current_character, enemy_character):
    draw_text(f"{current_character.name} HP: {current_character.health}",
              constants.FONT_GAMEPLAY, constants.SIZE_CHARACTERS_HEALTH,
              constants.COLOR_WHITE_TUPLE,
              constants.POSITION_X_CHARACTERS_HEALTH,
              constants.POSITION_Y_CURRENT_CHARACTER_HEALTH)
    draw_text(f"{enemy_character.name} HP: {enemy_character.health}",
              constants.FONT_GAMEPLAY, constants.SIZE_CHARACTERS_HEALTH,
              constants.COLOR_WHITE_TUPLE,
              constants.POSITION_X_CHARACTERS_HEALTH,
              constants.POSITION_Y_ENEMY_CHARACTER_HEALTH)


def draw_buttons(buttons):
    for button in buttons:
        button.draw()


def draw_characters(current_character, enemy_character):
    # Ajusta el tamaño de los sprites
    scale_factor = 3  # Aumenta el tamaño del sprite al 220%

    # Posiciones de los personajes
    current_character_x = (constants.WINDOW_WIDTH //
                           2) - 375  # Más a la izquierda
    current_character_y = constants.WINDOW_HEIGHT - 400  # Un poco más arriba

    enemy_character_x = (constants.WINDOW_WIDTH //
                         2) + 50  # Un poco más a la derecha
    enemy_character_y = (
        constants.WINDOW_HEIGHT - 650
    )  # Mantiene la altura original o ajústala si es necesario

    # Escala y dibuja los sprites
    window.blit(
        pygame.transform.scale(
            sprites[current_character.name]["back"],
            (
                int(sprites[current_character.name]["back"].get_width() *
                    scale_factor),
                int(sprites[current_character.name]["back"].get_height() *
                    scale_factor),
            ),
        ),
        (current_character_x, current_character_y),
    )

    enemy_character_size = (
        int(sprites[enemy_character.name]["front"].get_width() * scale_factor),
        int(sprites[enemy_character.name]["front"].get_height() * scale_factor),
    )

    window.blit(
        pygame.transform.scale(sprites[enemy_character.name]["front"],
                               enemy_character_size),
        (enemy_character_x, enemy_character_y),
    )


def draw_text(text, font, size, title_color, position_x, position_y):
    text_font = pygame.font.Font(constants.PATH_FONTS + font, size)
    text_surface = text_font.render(text, True, title_color)
    window.blit(text_surface, (position_x, position_y))


def calculate_centered_x_position(text, font_filename, font_size):
    font = pygame.font.Font(constants.PATH_FONTS + font_filename, font_size)
    text_surface = font.render(text, True, constants.COLOR_WHITE_TUPLE)
    return (window.get_width() - text_surface.get_width()) // 2


def position_buttons(first_option_button, second_option_button):
    total_width = (
        first_option_button.rect.width +
        second_option_button.rect.width) + constants.BUTTONS_SPACING_MAIN_MENU
    start_x = (window.get_width() - total_width) // 2

    # Asignar las posiciones a los botones
    first_option_button.rect.x = start_x
    first_option_button.rect.y = constants.POSITION_Y_BUTTONS_MAIN_MENU

    second_option_button.rect.x = (start_x + first_option_button.rect.width +
                                   constants.BUTTONS_SPACING_MAIN_MENU)
    second_option_button.rect.y = constants.POSITION_Y_BUTTONS_MAIN_MENU


def check_change_icon_cursor(required_button, *optional_buttons):
    # Obtener la posición del mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Comprobar si el cursor está sobre el botón obligatorio
    if required_button.rect.collidepoint(mouse_x, mouse_y):
        pygame.mouse.set_cursor(
            pygame.SYSTEM_CURSOR_HAND)  # Cursor de mano del sistema
        return  # No chequeamos más botones si estamos sobre el obligatorio

    # Comprobar los botones opcionales
    for button in optional_buttons:
        if button.rect.collidepoint(mouse_x, mouse_y):
            pygame.mouse.set_cursor(
                pygame.SYSTEM_CURSOR_HAND)  # Cursor de mano del sistema
            return

    # Si no se colisiona con ningún botón, se restablece el cursor
    pygame.mouse.set_cursor(
        pygame.SYSTEM_CURSOR_ARROW)  # Cursor de flecha del sistema
