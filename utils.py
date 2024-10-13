import constants, game_context, pygame

window = game_context.get_window()
sprites = game_context.get_sprites()

def display_message(message, x, y, font_size=40):
    font = pygame.font.Font(None, font_size)
    text = font.render(message, True, constants.COLOR_WHITE_TUPLE)
    window.blit(text, (x, y))

def draw_conditions(current_character, enemy_character):
    draw_text(f"{current_character.name} HP: {current_character.health}", 40, 50, 50)
    draw_text(f"{enemy_character.name} HP: {enemy_character.health}", 40, 50, 100)

def draw_buttons(buttons, mouse_pos):
    for button in buttons:
        button.draw(window, mouse_pos)

def draw_characters(current_character, enemy_character):
    # Ajusta el tamaño de los sprites
    scale_factor = 3  # Aumenta el tamaño del sprite al 220%

    # Posiciones de los personajes
    current_character_x = (constants.INITIAL_WIDTH // 2) - 375  # Más a la izquierda
    current_character_y = constants.INITIAL_HEIGHT - 400  # Un poco más arriba

    enemy_character_x = (constants.INITIAL_WIDTH // 2) + 50  # Un poco más a la derecha
    enemy_character_y = constants.INITIAL_HEIGHT - 650 # Mantiene la altura original o ajústala si es necesario

    # Escala y dibuja los sprites
    window.blit(pygame.transform.scale(sprites[current_character.name]['back'], 
               (int(sprites[current_character.name]['back'].get_width() * scale_factor), 
                int(sprites[current_character.name]['back'].get_height() * scale_factor))), 
                (current_character_x, current_character_y))

    enemy_character_size = (int(sprites[enemy_character.name]['front'].get_width() * scale_factor), 
                             int(sprites[enemy_character.name]['front'].get_height() * scale_factor))

    window.blit(pygame.transform.scale(sprites[enemy_character.name]['front'], enemy_character_size), 
                (enemy_character_x, enemy_character_y))

def draw_text(text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, constants.COLOR_BLACK_TUPLE)
    window.blit(text_surface, (x, y))
