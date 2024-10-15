import constants, game_context, pygame, utils
from background_animated import BackgroundAnimated
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
            return constants.QUIT_ACTION  # Indicar que se ha seleccionado salir del juego
        if event.type == pygame.MOUSEBUTTONDOWN:
            if confirm_button.is_clicked():  # Confirmar salida
                return constants.CONFIRM_ACTION  # Retornar cadena significativa
            if cancel_button.is_clicked():  # Cancelar, volver al menú principal
                return constants.CANCEL_ACTION  # Retornar cadena significativa
    return None  # Indicar que no se ha tomado ninguna acción


# =========================================== Funcion Principal ===========================================


def confirm_exit(background_animated=None):
    button_font = pygame.font.Font(
        constants.PATH_FONTS + constants.FONT_GAMEPLAY,
        constants.SIZE_FONT_BUTTONS_MAIN_MENU,
    )
    confirm_button, cancel_button = create_buttons(button_font)
    utils.position_buttons(confirm_button, cancel_button)

    # Establecer el cursor predeterminado al inicio
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    if (background_animated == None):
        background_animated = BackgroundAnimated(
            constants.PATH_BACKGROUND_ANIMATED, constants.FRAME_BASE_NAME,
            constants.FRAME_DELAY)

    waiting = True
    while waiting:
        # Actualizar y dibujar el fondo
        background_animated.update()
        background_animated.draw_background()

        # Mostrar el mensaje de confirmación de salida
        position_x_center = utils.calculate_centered_x_position(
            constants.MENSAJE_DE_CONFIRMACION_SALIDA, constants.FONT_GAMEPLAY,
            constants.SIZE_FONT_TITLE_CONFIRM_EXIT)

        utils.draw_text(constants.MENSAJE_DE_CONFIRMACION_SALIDA,
                        constants.FONT_GAMEPLAY,
                        constants.SIZE_FONT_TITLE_CONFIRM_EXIT,
                        constants.COLOR_WHITE_TUPLE, position_x_center,
                        constants.POSITION_Y_TITLE_CONFIRM_EXIT)

        # Dibujar los botones de confirmar y cancelar
        confirm_button.draw()
        cancel_button.draw()
        pygame.display.flip()

        utils.check_change_icon_cursor(confirm_button, cancel_button)

        # Manejar eventos
        action = handle_events(confirm_button, cancel_button)
        if action == constants.CANCEL_ACTION:  # Cancelar, volver al menú principal
            waiting = False  # Salir del bucle, volver al menú
        elif action == constants.CONFIRM_ACTION or action == constants.QUIT_ACTION:  # Confirmar salida o cerrar juego desde la ventana
            return action  # Cerrar el juego
