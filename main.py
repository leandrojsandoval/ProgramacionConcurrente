import battle
import copy
import constants
import exit_menu
import game_context
import main_menu
import pygame
import random
import selector_character_menu

pygame.init()
window = game_context.get_window()

def game_loop():
    while True:
        # Muestra el menú de selección de personajes
        action, selected_character = selector_character_menu.selector_menu()

        # Si el usuario selecciona salir, termina el bucle y devuelve la acción
        if action == constants.QUIT_ACTION:
            return action

        # Si se selecciona un personaje válido, se procede a la batalla
        elif selected_character is not None:
            
            # Filtra la lista de personajes disponibles, excluyendo el personaje seleccionado
            available_characters = [character for character in game_context.get_characters() if character != selected_character]
            
            # Selecciona un personaje enemigo al azar
            enemy_character = random.choice(available_characters)
            
            # Inicia la batalla entre el personaje seleccionado y el enemigo, haciendo copias profundas de ambos
            battle.start_battle(copy.deepcopy(selected_character), copy.deepcopy(enemy_character))

if __name__ == "__main__":
    while True:
        # Muestra el menú principal y espera la acción del jugador
        action = main_menu.show_start_screen()

        # Si el jugador elige jugar, inicia el bucle del juego
        if action == constants.PLAY_ACTION:
            game_running = game_loop()

            # Si la acción resultante del bucle es salir, termina el juego
            if game_running == constants.QUIT_ACTION:
                break

        # Si el jugador selecciona salir desde el menú principal
        elif action == constants.EXIT_ACTION:

            # Muestra un menú de confirmación para salir del juego
            result = exit_menu.confirm_exit()

            # Si el jugador confirma salir, se cierra el juego
            if result == constants.CONFIRM_ACTION or result == constants.QUIT_ACTION:
                break   # Termina el programa
        
        # Si el jugador cancela la salida, vuelve al menú principal sin cerrar el juego

    pygame.quit()
