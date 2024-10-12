import battle, game_context, menu_selector, pygame, random

pygame.init()

window = game_context.get_window()

bg_image = pygame.image.load('assets/background_bosque.png')

if __name__ == "__main__":

    selected_character = menu_selector.main_menu()
    
    if selected_character:
        available_characters = [character for name, character in game_context.get_characters().items() if character != selected_character]
        enemy_character = random.choice(available_characters) if available_characters else None
        if enemy_character:
            battle.start_battle(selected_character, enemy_character, bg_image)
        else:
            print("No hay enemigos disponibles para la batalla.")
    else:
        print("No se seleccionó ningún personaje.")
    
    pygame.quit()
