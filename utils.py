import constants, game_context, pygame

window = game_context.get_window()
sprites = game_context.get_sprites()

def draw_conditions(current_character, enemy_character):
    draw_text(f"{current_character.name} HP: {current_character.health}", 40, 50, 50)
    draw_text(f"{enemy_character.name} HP: {enemy_character.health}", 40, 50, 100)

def draw_buttons(buttons, mouse_pos):
    for button in buttons:
        button.draw(window, mouse_pos)

def draw_characters(current_character, enemy_character):
    current_character_x = constants.INITIAL_WIDTH // 2
    enemy_character_x = constants.INITIAL_WIDTH // 2
    enemy_character_size = (int(sprites[enemy_character.name]['front'].get_width() * 1.5), int(sprites[enemy_character.name]['front'].get_height() * 1.5))

    window.blit(sprites[current_character.name]['back'], (current_character_x, constants.INITIAL_HEIGHT - 200))

    window.blit(pygame.transform.scale(sprites[enemy_character.name]['front'], enemy_character_size), (enemy_character_x, constants.INITIAL_HEIGHT - 600))

def draw_text(text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, constants.BLACK)
    window.blit(text_surface, (x, y))
