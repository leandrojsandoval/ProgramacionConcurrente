import constants, game_context, pygame
from button import Button
import os

#=========================================== Variables ===========================================

window = game_context.get_window()

#=========================================== Animacion ===========================================

def load_animation_frames(path_frames, frame_base_name):
    frames = []
    all_files = os.listdir(path_frames)
    for file_name in all_files:
        if file_name.startswith(frame_base_name) and file_name.endswith(".png"):
            frame_path = os.path.join(path_frames, file_name)
            frame_image = pygame.image.load(frame_path)
            frame_image = pygame.transform.scale(frame_image, (window.get_width(), window.get_height()))
            frames.append(frame_image)
    return frames

def update_background_animation(frames, current_frame, frame_counter, frame_delay):
    frame_counter += 1
    if frame_counter >= frame_delay:
        frame_counter = 0
        current_frame = (current_frame + 1) % len(frames)
    window.blit(frames[current_frame], (0, 0))
    return current_frame, frame_counter

#=========================================== Dibujo ===========================================

def draw_title(title, title_font, title_color, title_x, title_y):
    title_text = title_font.render(title, True, title_color)
    window.blit(title_text, (title_x, title_y))

def position_buttons(play_button, exit_button):
    total_width = (play_button.rect.width + exit_button.rect.width) + constants.BUTTONS_SPACING_MAIN_MENU
    start_x = (window.get_width() - total_width) // 2

    # Asignar las posiciones a los botones
    play_button.rect.x = start_x
    play_button.rect.y = constants.POSITION_Y_BUTTONS_MAIN_MENU

    exit_button.rect.x = start_x + play_button.rect.width + constants.BUTTONS_SPACING_MAIN_MENU
    exit_button.rect.y = constants.POSITION_Y_BUTTONS_MAIN_MENU

#=========================================== Eventos ===========================================

def handle_events(play_button, exit_button):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.is_clicked(pygame.mouse.get_pos()):
                return "play"
            if exit_button.is_clicked(pygame.mouse.get_pos()):
                return "exit"
    return None

#=========================================== Funcion Principal ===========================================

def show_start_screen():

    # Inicialización de fuentes y botones
    title_font = pygame.font.Font(constants.PATH_FONTS + constants.FONT_GAMEPLAY, constants.SIZE_FONT_TITLE_MAIN_MENU)
    button_font = pygame.font.Font(constants.PATH_FONTS + constants.FONT_GAMEPLAY, constants.SIZE_FONT_BUTTONS_MAIN_MENU)
    play_button = Button(constants.JUGAR, 0, 300, 200, 50, constants.COLOR_GREEN_TUPLE, constants.COLOR_LIGHT_GREEN_TUPLE, constants.COLOR_BLACK_TUPLE, constants.PIXELS_BORDER_BUTTON, font=button_font)
    exit_button = Button(constants.SALIR, 0, 300, 200, 50, constants.COLOR_RED_TUPLE, constants.COLOR_LIGHT_RED_TUPLE, constants.COLOR_BLACK_TUPLE, constants.PIXELS_BORDER_BUTTON, font=button_font)

    # Cargar los cuadros de animación del fondo
    frames = load_animation_frames(constants.PATH_BACKGROUND_ANIMATED, constants.FRAME_BASE_NAME)
    current_frame = 0  # Cuadro inicial de la animación
    frame_counter = 0  # Contador para manejar la animación

    # Cálculo de la posición del título en el centro de la pantalla
    title_text = title_font.render(constants.GAME_NAME, True, constants.COLOR_WHITE_TUPLE)
    title_x = (window.get_width() - title_text.get_width()) // 2

    # Posicionar los botones en la pantalla
    position_buttons(play_button, exit_button)

    while True:
        current_frame, frame_counter = update_background_animation(frames, current_frame, frame_counter, constants.FRAME_DELAY)

        draw_title(constants.GAME_NAME, title_font, constants.COLOR_WHITE_TUPLE , title_x, constants.POSITION_Y_TITLE_MAIN_MENU)
        play_button.draw(window, pygame.mouse.get_pos())
        exit_button.draw(window, pygame.mouse.get_pos())
        pygame.display.flip()

        result = handle_events(play_button, exit_button)
        if result is not None:
            return result
