import constants, game_context, os, pygame

window = game_context.get_window()
sprites = game_context.get_sprites()


def display_message(message, x, y, font_size=40):
    font = pygame.font.Font(None, font_size)
    text = font.render(message, True, constants.COLOR_WHITE_TUPLE)
    window.blit(text, (x, y))


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
        int(sprites[enemy_character.name]["front"].get_height() *
            scale_factor),
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


def get_center_text_position_x(text_width):
    return (window.get_width() - text_width) // 2


def calculate_centered_x_position(text, font_filename, font_size):
    font = pygame.font.Font(constants.PATH_FONTS + font_filename, font_size)
    text_surface = font.render(text, True, constants.COLOR_WHITE_TUPLE)
    return (window.get_width() - text_surface.get_width()) // 2


def split_text(text):
    words = text.split()
    return words


def position_buttons(first_option_button, second_option_button):
    total_width = (
        first_option_button.rect.width +
        second_option_button.rect.width) + constants.BUTTONS_SPACING_MAIN_MENU
    start_x = get_center_text_position_x(total_width)

    # Asignar las posiciones a los botones
    first_option_button.rect.x = start_x
    first_option_button.rect.y = constants.POSITION_Y_BUTTONS_MAIN_MENU

    second_option_button.rect.x = (start_x + first_option_button.rect.width +
                                   constants.BUTTONS_SPACING_MAIN_MENU)
    second_option_button.rect.y = constants.POSITION_Y_BUTTONS_MAIN_MENU


def load_animation_frames(path_frames, frame_base_name):
    frames = []
    all_files = os.listdir(path_frames)
    for file_name in all_files:
        if file_name.startswith(frame_base_name) and file_name.endswith(
                constants.EXTENSION_PNG):
            frame_path = os.path.join(path_frames, file_name)
            frame_image = pygame.image.load(frame_path)
            frame_image = pygame.transform.scale(
                frame_image, (window.get_width(), window.get_height()))
            frames.append(frame_image)
    return frames


def update_background_animation(frames, current_frame, frame_counter,
                                frame_delay):
    frame_counter += 1
    if frame_counter >= frame_delay:
        frame_counter = 0
        current_frame = (current_frame + 1) % len(frames)
    window.blit(frames[current_frame], (0, 0))
    return current_frame, frame_counter
