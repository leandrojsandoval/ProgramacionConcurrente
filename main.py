import battle, copy, constants, exit_menu, main_menu, game_context, pygame, random, selector_character_menu

pygame.init()
window = game_context.get_window()

def game_loop():
    running = True
    while running:
        action, selected_character = selector_character_menu.selector_menu()
        if action == constants.QUIT_ACTION: # Si el usuario elige salir
            running = False
            return action
        elif selected_character != None:
            available_characters = [character for character in game_context.get_characters() if character != selected_character]
            enemy_character = random.choice(available_characters)
            battle.start_battle(copy.deepcopy(selected_character), copy.deepcopy(enemy_character))

if __name__ == "__main__":
    while True:  # Mantén este bucle para poder regresar al menú
        action = main_menu.show_start_screen()
        if action == constants.PLAY_ACTION:
            game_running = game_loop()
            if game_running == constants.QUIT_ACTION:  # Si la acción es salir, terminamos el juego
                break
        elif action == constants.EXIT_ACTION:
            result = exit_menu.confirm_exit()
            if result == constants.CONFIRM_ACTION or result == constants.QUIT_ACTION:
                break  # Cierra el juego si el usuario confirma la salida o cierra la ventana
            # Si `confirm_exit` devuelve "cancel", volvemos al menú sin cerrar
    pygame.quit()