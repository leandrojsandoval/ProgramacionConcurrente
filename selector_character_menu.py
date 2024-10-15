import constants, exit_menu, game_context, pygame, utils

# =========================================== Variables ===========================================

bg_image = pygame.image.load(constants.PATH_BACKGROUNDS + "background_waterfalls.jpg")
bg_image = pygame.transform.scale(bg_image, (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
characters = game_context.get_characters()
current_selection = 0
first_visible_index = 0  # Índice del primer personaje visible
window = game_context.get_window()

# =========================================== Interfaz ===========================================


def load_list_characters(sprites):
    for i in range(first_visible_index, min(first_visible_index + constants.VISIBLE_CHARACTERS_COUNT, len(characters))):
        character = characters[i]
        utils.draw_text(character.name,
                        constants.FONT_GAMEPLAY,
                        constants.SIZE_FONT_CHARACTERS,
                        constants.COLOR_BLACK_TUPLE,
                        250,
                        200 + (i - first_visible_index) * 100)
        if current_selection == i:
            pygame.draw.rect(window, constants.COLOR_BLACK_TUPLE, (240, 190 + (i - first_visible_index) * 100, 300, 50), 2)

    # Dibuja el sprite del personaje seleccionado en una posición fija
    selected_character = characters[current_selection]
    try:
        image_to_draw = sprites[selected_character.name]["front"]
        scaled_image = pygame.transform.scale(image_to_draw, (constants.SIZE_X_CHARACTER_SELECTED, constants.SIZE_Y_CHARACTER_SELECTED))
        window.blit(scaled_image, (constants.POSITION_X_SPRITE_CHARACTER_SELECTED, constants.POSITION_Y_SPRITE_CHARACTER_SELECTED))
    except KeyError:
        print(f"Error: El personaje {selected_character.name} no tiene sprite cargado.")
    except Exception as e:
        print(f"Error al dibujar la imagen: {e}")


# =========================================== Eventos ===========================================

def update_index():
    global current_selection, first_visible_index
    if current_selection < first_visible_index:
        first_visible_index = current_selection
    elif (current_selection >= first_visible_index + constants.VISIBLE_CHARACTERS_COUNT):
        first_visible_index = (current_selection - constants.VISIBLE_CHARACTERS_COUNT + 1)

def handle_events():
    global current_selection, first_visible_index

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            result = exit_menu.confirm_exit()
            if result == constants.CONFIRM_ACTION or result == constants.QUIT_ACTION:
                return constants.QUIT_ACTION, None  # Retornar acción y ningún personaje
            else:
                return None, None  # No hace nada, sigue en el menú de selección

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_UP):
                direction = 1 if event.key == pygame.K_DOWN else -1
                current_selection = (current_selection + direction) % constants.NUMBER_OF_CHARACTERS

                # Actualizar el índice de desplazamiento visible
                update_index()

            elif event.key == pygame.K_RETURN:
                return constants.SELECT_CHARACTER_ACTION, characters[current_selection]  # Acción de selección de personaje

    return None, None  # Si no se ha realizado ninguna acción


# =========================================== Funcion Principal ===========================================

def selector_menu():
    # Establecer el cursor predeterminado al inicio
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    running = True
    while running:
        window.fill(constants.COLOR_WHITE_TUPLE)
        window.blit(bg_image, (0, 0))
        utils.draw_text(constants.ELIGE_TU_PERSONAJE,
                        constants.FONT_GAMEPLAY,
                        constants.SIZE_FONT_TITLE_CHARACTER,
                        constants.COLOR_BLACK_TUPLE,
                        250,
                        50)
        load_list_characters(game_context.get_sprites())

        action, selected_character = handle_events()

        if action == constants.QUIT_ACTION:
            running = False  # Termina el ciclo principal
        elif action == constants.SELECT_CHARACTER_ACTION and selected_character is not None:
            return action, selected_character  # Devuelve el personaje seleccionado y sale del menú

        pygame.display.update()
    
    return action, None
