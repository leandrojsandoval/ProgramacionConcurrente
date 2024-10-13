import game_context, main_menu, pygame, utils
from button import Button

window = game_context.get_window()

def confirm_exit():
    """Función para confirmar si el usuario desea salir."""
    exit_button = Button("Sí", 250, 200, 200, 50, (128, 0, 0), (255, 0, 0))
    cancel_button = Button("No", 250, 300, 200, 50, (0, 128, 0), (0, 255, 0))

    window.fill((0, 0, 0))  # Limpiar la pantalla con color negro
    utils.display_message("¿Estás seguro que deseas salir?", 100, 100, font_size=40)
    exit_button.draw(window, pygame.mouse.get_pos())
    cancel_button.draw(window, pygame.mouse.get_pos())
    pygame.display.flip()  # Cambia a flip para actualizar la pantalla

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if exit_button.is_clicked(mouse_pos):  # Confirmar salida
                    return False
                if cancel_button.is_clicked(mouse_pos):  # No salir
                    waiting = False
                    main_menu.show_start_screen()  # Volver a la pantalla de inicio