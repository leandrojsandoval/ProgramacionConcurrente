import battle, exit_menu, main_menu, game_context, selector_character_menu, pygame, random, utils

pygame.init()
window = game_context.get_window()


def game_loop():
    running = True
    while running:
        selected_character = selector_character_menu.main_menu()

        if selected_character:
            available_characters = [
                character
                for name, character in game_context.get_characters().items()
                if character != selected_character
            ]
            enemy_character = (random.choice(available_characters)
                               if available_characters else None)
            if enemy_character:
                battle.start_battle(selected_character, enemy_character)
            else:
                print("No hay enemigos disponibles para la batalla.")

        # Mostrar mensaje en pantalla
        window.fill((0, 0, 0))  # Limpiar la pantalla con color negro
        utils.display_message("¿Quieres jugar otra batalla? (s/n)",
                              100,
                              200,
                              font_size=50)

        if not wait_for_input():  # Ahora esta función está definida
            running = False


def wait_for_input():
    """Función para esperar la entrada del usuario con clic en el mouse."""
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Salir del juego
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 es el botón izquierdo del mouse
                    waiting = False  # Terminar la espera
                    return True  # Continuar
    return True  # Continuar si no se cierra la ventana


if __name__ == "__main__":
    action = main_menu.show_start_screen()
    if action == "play":
        game_loop()
    elif action == "exit":
        if not exit_menu.confirm_exit():
            print("Juego cerrado")
    pygame.quit()
