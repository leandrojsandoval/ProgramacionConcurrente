import constants, exit_menu, game_context, pygame, utils
from button import Button
import os

# =========================================== Variables ===========================================

window = game_context.get_window()

# =========================================== Interfaz ===========================================


def create_buttons(button_font):
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
    return play_button, exit_button


def show_game_name_by_words(words):
    position_y = constants.POSITION_Y_TITLE_MAIN_MENU
    spacing = constants.SIZE_FONT_TITLE_MAIN_MENU + constants.SPACING_Y_BY_WORD
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
                return constants.PLAY_ACTION
            if exit_button.is_clicked():
                return constants.EXIT_ACTION

    utils.check_change_icon_cursor(play_button, exit_button)

    return None


# =========================================== Funcion Principal ===========================================


def show_start_screen():
    # Inicialización de fuentes y botones
    button_font = pygame.font.Font(
        constants.PATH_FONTS + constants.FONT_GAMEPLAY,
        constants.SIZE_FONT_BUTTONS_MAIN_MENU,
    )
    play_button, exit_button = create_buttons(button_font)

    # Posicionar los botones en la pantalla
    utils.position_buttons(play_button, exit_button)

    # Cargar los cuadros de animación del fondo
    frames = utils.load_animation_frames(constants.PATH_BACKGROUND_ANIMATED,
                                         constants.FRAME_BASE_NAME)
    current_frame = 0  # Cuadro inicial de la animación
    frame_counter = 0  # Contador para manejar la animación

    words_game_name = utils.split_text(constants.GAME_NAME)

    # Establecer el cursor predeterminado al inicio
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    while True:
        # Animar el fondo
        current_frame, frame_counter = utils.update_background_animation(
            frames, current_frame, frame_counter, constants.FRAME_DELAY)
        show_game_name_by_words(words_game_name)
        play_button.draw()
        exit_button.draw()

        pygame.display.flip()

        # Manejar eventos
        result = handle_events(play_button, exit_button)
        if result == constants.PLAY_ACTION:
            return result
        elif result == constants.EXIT_ACTION:
            if not exit_menu.confirm_exit(frames, current_frame,
                                          frame_counter):
                return  # Salir del juego si se confirma la salida
            # Si se cancela la salida, se continúa mostrando el menú principal
