import constants, game_context, pygame, utils

bg_image = pygame.image.load('assets/background_waterfalls.jpg')
characters = game_context.get_characters()
current_selection = 0
window = game_context.get_window()

def load_list_characters(sprites):
    for i, character in enumerate(characters.values()):
        utils.draw_text(character.name, 40, 250, 200 + i * 100)
        if current_selection == i:
            pygame.draw.rect(window, constants.BLACK, (240, 190 + i * 100, 300, 50), 2)
            try:
                image_to_draw = sprites[character.name]['front']
                # Escalar la imagen a un tamaño mayor (por ejemplo, 180x180)
                scaled_image = pygame.transform.scale(image_to_draw, (180, 180))
                # Modificar la posición de dibujo (más abajo)
                window.blit(scaled_image, (650, 280))  # Cambia y a 280
            except KeyError:
                print(f"Error: El personaje {character.name} no tiene sprite cargado.")
            except Exception as e:
                print(f"Error al dibujar la imagen: {e}")

def handle_events():
    global current_selection
    # Obtener las claves del diccionario en una lista
    characters_names = list(characters.keys())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return None
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_UP):
                direction = 1 if event.key == pygame.K_DOWN else -1
                current_selection = (current_selection + direction) % len(characters_names)
            elif event.key == pygame.K_RETURN:
                # Devuelve el personaje correspondiente al nombre seleccionado
                selected_name = characters_names[current_selection]
                return characters[selected_name]
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for i, name in enumerate(characters_names):
                # Verificar si el mouse está sobre el área del personaje
                if 250 <= mouse_x <= 550 and (200 + i * 100) <= mouse_y < (250 + i * 100):
                    return characters[name]  # Devuelve el personaje correspondiente al nombre
    return None

def main_menu():
    running = True
    while running:
        window.fill(constants.WHITE)
        window.blit(bg_image, (0, 0))
        utils.draw_text("Elige tu Personaje", 60, 250, 50)
        load_list_characters(game_context.get_sprites())
        selected_character = handle_events()
        if selected_character is not None:
            return selected_character
        pygame.display.update()
