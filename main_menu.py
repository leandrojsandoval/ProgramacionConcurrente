import constants, game_context, pygame, utils
from button import Button
import os

# =========================================== Variables ===========================================

window = game_context.get_window()

# =========================================== Animacion ===========================================


def load_animation_frames(path_frames, frame_base_name):
    frames = []
    all_files = os.listdir(path_frames)
    for file_name in all_files:
        if file_name.startswith(frame_base_name) and file_name.endswith(
                ".png"):
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


# =========================================== Dibujo ===========================================


def position_buttons(play_button, exit_button):
    total_width = (play_button.rect.width + exit_button.rect.width
                   ) + constants.BUTTONS_SPACING_MAIN_MENU
    start_x = utils.get_center_text_position_x(total_width)

    # Asignar las posiciones a los botones
    play_button.rect.x = start_x
    play_button.rect.y = constants.POSITION_Y_BUTTONS_MAIN_MENU

    exit_button.rect.x = (start_x + play_button.rect.width +
                          constants.BUTTONS_SPACING_MAIN_MENU)
    exit_button.rect.y = constants.POSITION_Y_BUTTONS_MAIN_MENU


def show_game_name_by_words(words):
    position_y = constants.POSITION_Y_TITLE_MAIN_MENU
    spacing = constants.SIZE_FONT_TITLE_MAIN_MENU + 10

    for word in words:
        position_x = utils.calculate_centered_x_position(
            word, constants.FONT_GAMEPLAY, constants.SIZE_FONT_TITLE_MAIN_MENU)
        utils.draw_text(word, constants.FONT_GAMEPLAY,
                        constants.SIZE_FONT_TITLE_MAIN_MENU,
                        constants.COLOR_WHITE_TUPLE, position_x, position_y)
        position_y += spacing


# =========================================== Eventos ===========================================


def handle_events(play_button, exit_button):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.is_clicked():
                return "play"
            if exit_button.is_clicked():
                return "exit"
    return None


# =========================================== Funcion Principal ===========================================


def show_start_screen():

    # Inicialización de fuentes y botones
    button_font = pygame.font.Font(
        constants.PATH_FONTS + constants.FONT_GAMEPLAY,
        constants.SIZE_FONT_BUTTONS_MAIN_MENU,
    )
    play_button = Button(
        constants.JUGAR,
        0,
        300,
        200,
        50,
        constants.COLOR_GREEN_TUPLE,
        constants.COLOR_LIGHT_GREEN_TUPLE,
        constants.COLOR_BLACK_TUPLE,
        constants.PIXELS_BORDER_BUTTON,
        font=button_font,
    )
    exit_button = Button(
        constants.SALIR,
        0,
        300,
        200,
        50,
        constants.COLOR_RED_TUPLE,
        constants.COLOR_LIGHT_RED_TUPLE,
        constants.COLOR_BLACK_TUPLE,
        constants.PIXELS_BORDER_BUTTON,
        font=button_font,
    )

    # Posicionar los botones en la pantalla
    position_buttons(play_button, exit_button)

    # Cargar los cuadros de animación del fondo
    frames = load_animation_frames(constants.PATH_BACKGROUND_ANIMATED,
                                   constants.FRAME_BASE_NAME)
    current_frame = 0  # Cuadro inicial de la animación
    frame_counter = 0  # Contador para manejar la animación

    words_game_name = utils.split_text(constants.GAME_NAME)

    while True:
        current_frame, frame_counter = update_background_animation(
            frames, current_frame, frame_counter, constants.FRAME_DELAY)

        show_game_name_by_words(words_game_name)

        play_button.draw()
        exit_button.draw()
        pygame.display.flip()

        result = handle_events(play_button, exit_button)
        if result is not None:
            return result
