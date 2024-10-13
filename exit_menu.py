import constants, game_context, pygame, utils
from button import Button

window = game_context.get_window()


def confirm_exit(frames, current_frame, frame_counter):
    button_font = pygame.font.Font(
        constants.PATH_FONTS + constants.FONT_GAMEPLAY,
        constants.SIZE_FONT_BUTTONS_MAIN_MENU,
    )
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

        # Obtener la posición del mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Cambiar el cursor según la posición del mouse
        if confirm_button.rect.collidepoint(mouse_x, mouse_y) or cancel_button.rect.collidepoint(mouse_x, mouse_y):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Cursor de mano del sistema
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Cursor de flecha del sistema

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Salir del juego completamente
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if confirm_button.is_clicked():  # Confirmar salida
                    pygame.quit(
                    )  # O realizar otra acción para cerrar el juego
                    return False
                if cancel_button.is_clicked(
                ):  # Cancelar, volver al menú principal
                    waiting = False
                    return True  # Indicar que se debe volver al menú principal
