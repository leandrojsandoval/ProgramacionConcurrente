import constants, game_context, pygame, utils
from button import Button

window = game_context.get_window()

# =========================================== Interfaz ===========================================


def create_buttons(button_font):
    confirm_button = Button(
        constants.ACEPTAR,
        0,
        300,
        200,
        50,
        constants.COLOR_ORANGE_TUPLE,
        constants.COLOR_LIGHT_ORANGE_TUPLE,
        constants.COLOR_BLACK_TUPLE,
        constants.PIXELS_BORDER_BUTTON,
        font=button_font,
    )
    cancel_button = Button(
        constants.CANCELAR,
        0,
        300,
        200,
        50,
        constants.COLOR_VIOLET_TUPLE,
        constants.COLOR_LIGHT_VIOLET_TUPLE,
        constants.COLOR_BLACK_TUPLE,
        constants.PIXELS_BORDER_BUTTON,
        font=button_font,
    )
    return confirm_button, cancel_button


# =========================================== Eventos ===========================================


def handle_events(confirm_button, cancel_button):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # Salir del juego completamente
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if confirm_button.is_clicked():  # Confirmar salida
                pygame.quit()  # O realizar otra acción para cerrar el juego
                return False
            if cancel_button.is_clicked(
            ):  # Cancelar, volver al menú principal
                return True  # Indicar que se debe volver al menú principal
    return None  # Para indicar que no se ha tomado ninguna acción


# =========================================== Funcion Principal ===========================================


def confirm_exit(frames, current_frame, frame_counter):
    button_font = pygame.font.Font(
        constants.PATH_FONTS + constants.FONT_GAMEPLAY,
        constants.SIZE_FONT_BUTTONS_MAIN_MENU,
    )
    confirm_button, cancel_button = create_buttons(button_font)
    utils.position_buttons(confirm_button, cancel_button)

    # Establecer el cursor predeterminado al inicio
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    waiting = True
    while waiting:
        # Continuar la animación del fondo
        current_frame, frame_counter = utils.update_background_animation(
            frames, current_frame, frame_counter, constants.FRAME_DELAY)

        # Mostrar el mensaje de confirmación de salida
        utils.draw_text(
            constants.MENSAJE_DE_CONFIRMACION_SALIDA, constants.FONT_GAMEPLAY,
            constants.SIZE_FONT_TITLE_CONFIRM_EXIT,
            constants.COLOR_WHITE_TUPLE,
            utils.calculate_centered_x_position(
                constants.MENSAJE_DE_CONFIRMACION_SALIDA,
                constants.FONT_GAMEPLAY,
                constants.SIZE_FONT_TITLE_CONFIRM_EXIT),
            constants.POSITION_Y_TITLE_CONFIRM_EXIT)

        # Dibujar los botones de confirmar y cancelar
        confirm_button.draw()
        cancel_button.draw()
        pygame.display.flip()

        utils.check_change_icon_cursor(confirm_button, cancel_button)

        # Manejar eventos
        action = handle_events(confirm_button, cancel_button)
        if action is True:  # Cancelar, volver al menú principal
            waiting = False  # Salir del bucle, volver al menú
        elif action is False:  # Confirmar salida
            return False  # Cerrar el juego

    return True  # Volver al menú principal (en caso de que la lógica lo requiera)
