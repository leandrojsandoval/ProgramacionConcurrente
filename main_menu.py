import constants
import game_context
import pygame
import utils
from button import Button
from background_animated import BackgroundAnimated

# =========================================== Variables ===========================================

window = game_context.get_window()

# =========================================== Interfaz ===========================================

def create_buttons():
    """
    Crea los botones de 'Jugar' y 'Salir' con sus respectivas propiedades, 
    como tamaño, colores y fuente, y los devuelve.

    Returns: tuple: Tupla que contiene el botón de 'Jugar' y el botón de 'Salir'.
    """
    
    # Inicialización de la fuente de los botones
    button_font = pygame.font.Font(
        constants.PATH_FONTS + constants.FONT_GAMEPLAY,
        constants.SIZE_FONT_BUTTONS_MAIN_MENU,
    )

    play_button = Button(
        constants.JUGAR,
        constants.POSITION_X_MAIN_MENU_BUTTONS,
        constants.POSITION_Y_MAIN_MENU_BUTTONS,
        constants.WIDTH_MAIN_MENU_BUTTONS,
        constants.HEIGHT_MAIN_MENU_BUTTONS,
        constants.COLOR_GREEN_TUPLE,
        constants.COLOR_LIGHT_GREEN_TUPLE,
        constants.COLOR_BLACK_TUPLE,
        constants.PIXELS_BORDER_BUTTON,
        font = button_font,
    )

    exit_button = Button(
        constants.SALIR,
        constants.POSITION_X_MAIN_MENU_BUTTONS,
        constants.POSITION_Y_MAIN_MENU_BUTTONS,
        constants.WIDTH_MAIN_MENU_BUTTONS,
        constants.HEIGHT_MAIN_MENU_BUTTONS,
        constants.COLOR_RED_TUPLE,
        constants.COLOR_LIGHT_RED_TUPLE,
        constants.COLOR_BLACK_TUPLE,
        constants.PIXELS_BORDER_BUTTON,
        font = button_font,
    )

    # Posicionar los botones en la pantalla
    utils.position_buttons(play_button, exit_button)

    return play_button, exit_button

def show_game_name_by_words(words):
    """
    Muestra el nombre del juego palabra por palabra, cada una en una línea diferente.

    Args: words (list): Lista de palabras que componen el nombre del juego.
    """
    position_y = constants.POSITION_Y_TITLE_MAIN_MENU
    
    # Espaciado entre palabras
    spacing = constants.SIZE_FONT_TITLE_MAIN_MENU + constants.SPACING_Y_BY_WORD

    for word in words:

        # Calcula la posición X para centrar cada palabra
        position_x = utils.calculate_centered_x_position(word, constants.FONT_GAMEPLAY, constants.SIZE_FONT_TITLE_MAIN_MENU)

        # Dibuja la palabra en pantalla
        utils.draw_text(
            word,
            constants.FONT_GAMEPLAY,
            constants.SIZE_FONT_TITLE_MAIN_MENU,
            constants.COLOR_WHITE_TUPLE,
            position_x,
            position_y
        )

        # Aumenta la posición Y para la siguiente palabra
        position_y += spacing

# =========================================== Eventos ===========================================

def handle_events(play_button, exit_button):
    """
    Maneja los eventos del menú, la interacción con los botones y el cierre de la ventana.

    Args:
        play_button (Button): Botón de 'Jugar'.
        exit_button (Button): Botón de 'Salir'.

    Returns: str: Retorna la acción seleccionada ('play' o 'exit') o None si no hubo acción.
    """
    action = None

    # Recorre la lista de eventos
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            # Si se cierra la ventana, establece la acción como salir
            action = constants.EXIT_ACTION
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            # Si se hace clic en el botón de 'Jugar', establece la acción como jugar
            if play_button.is_clicked():
                action = constants.PLAY_ACTION
            
            # Si se hace clic en el botón de 'Salir', establece la acción como salir
            elif exit_button.is_clicked():
                action = constants.EXIT_ACTION

    # Verifica si el cursor debe cambiar dependiendo de si está sobre algún botón
    utils.check_change_icon_cursor(play_button, exit_button)

    return action

# =========================================== Función Principal ===========================================

def show_start_screen():
    """
    Muestra la pantalla de inicio del juego, incluyendo el fondo animado, 
    el título y los botones de 'Jugar' y 'Salir'.
    
    Retorna:
        str: La acción seleccionada ('play' o 'exit').
    """
    play_button, exit_button = create_buttons()

    # Crear la instancia de BackgroundAnimation
    background_animated = BackgroundAnimated(constants.PATH_BACKGROUND_ANIMATED,
                                             constants.FRAME_BASE_NAME,
                                             constants.FRAME_DELAY)

    words_game_name = constants.GAME_NAME.split()

    # Establecer el cursor predeterminado al inicio
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    while True:

        # Actualiza y dibuja el fondo animado
        background_animated.update()
        background_animated.draw_background()

        # Muestra el nombre del juego palabra por palabra
        show_game_name_by_words(words_game_name)

        # Dibuja los botones de 'Jugar' y 'Salir'
        play_button.draw()
        exit_button.draw()

        # Actualiza la pantalla
        pygame.display.flip()

        # Maneja los eventos (clic en botones, cierre de ventana, etc.)
        result = handle_events(play_button, exit_button)

        # Si el jugador selecciona 'Jugar' o 'Salir', retorna la acción
        if result == constants.PLAY_ACTION or result == constants.EXIT_ACTION:
            return result
