import battle, copy, exit_menu, main_menu, game_context, selector_character_menu, pygame, random, utils

pygame.init()
window = game_context.get_window()


def game_loop():
    running = True
    while running:
        selected_character = selector_character_menu.main_menu()

        if selected_character:
            available_characters = [
                character
                for character in game_context.get_characters()  # Ahora es una lista
                if character != selected_character
            ]
            enemy_character = random.choice(available_characters)
            battle.start_battle(copy.deepcopy(selected_character),
                                copy.deepcopy(enemy_character))


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
