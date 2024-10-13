import constants, game_context, pygame, utils

# =========================================== Variables ===========================================

bg_image = pygame.image.load(constants.NAME_FOLDER_BACKGROUNDS +
                             "/background_waterfalls.jpg")
bg_image = pygame.transform.scale(
    bg_image, (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
characters = game_context.get_characters()
current_selection = 0
first_visible_index = 0  # Índice del primer personaje visible
visible_characters_count = 5  # Número de personajes visibles en la pantalla
window = game_context.get_window()

# =========================================== Interfaz ===========================================


def load_list_characters(sprites):
    for i in range(
            first_visible_index,
            min(first_visible_index + visible_characters_count,
                len(characters)),
    ):
        character = list(characters.values())[i]
        utils.draw_text(character.name, constants.FONT_GAMEPLAY,
                        constants.SIZE_FONT_CHARACTERS,
                        constants.COLOR_BLACK_TUPLE, 250,
                        200 + (i - first_visible_index) * 100)
        if current_selection == i:
            pygame.draw.rect(
                window,
                constants.COLOR_BLACK_TUPLE,
                (240, 190 + (i - first_visible_index) * 100, 300, 50),
                2,
            )

    # Dibuja el sprite del personaje seleccionado en una posición fija
    selected_character = list(characters.values())[current_selection]
    try:
        image_to_draw = sprites[selected_character.name]["front"]
        scaled_image = pygame.transform.scale(
            image_to_draw, (constants.SIZE_X_CHARACTER_SELECTED,
                            constants.SIZE_Y_CHARACTER_SELECTED))
        window.blit(
            scaled_image,
            (
                constants.POSITION_X_SPRITE_CHARACTER_SELECTED,
                constants.POSITION_Y_SPRITE_CHARACTER_SELECTED,
            ),
        )
    except KeyError:
        print(
            f"Error: El personaje {selected_character.name} no tiene sprite cargado."
        )
    except Exception as e:
        print(f"Error al dibujar la imagen: {e}")


# =========================================== Eventos ===========================================


def handle_events():
    global current_selection, first_visible_index
    characters_names = list(characters.keys())
    total_characters = len(characters_names)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "QUIT"  # Devuelve "QUIT" para indicar que el usuario quiere cerrar el juego

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_UP):
                direction = 1 if event.key == pygame.K_DOWN else -1
                current_selection = (
                    current_selection +
                    direction) % total_characters  # Movimiento circular

                # Actualizar el índice de desplazamiento visible
                if current_selection < first_visible_index:
                    first_visible_index = current_selection
                elif (current_selection
                      >= first_visible_index + visible_characters_count):
                    first_visible_index = (current_selection -
                                           visible_characters_count + 1)

            elif event.key == pygame.K_RETURN:
                selected_name = characters_names[current_selection]
                return characters[selected_name]

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for i, name in enumerate(
                    characters_names[first_visible_index:first_visible_index +
                                     visible_characters_count]):
                if 250 <= mouse_x <= 550 and (200 + i * 100) <= mouse_y < (
                        250 + i * 100):
                    current_selection = first_visible_index + i
                    return characters[name]

    return None


# =========================================== Funcion Principal ===========================================


def main_menu():
    # Establecer el cursor predeterminado al inicio
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    running = True
    while running:
        window.fill(constants.COLOR_WHITE_TUPLE)
        window.blit(bg_image, (0, 0))
        utils.draw_text(constants.ELIGE_TU_PERSONAJE, constants.FONT_GAMEPLAY,
                        constants.SIZE_FONT_TITLE_CHARACTER,
                        constants.COLOR_BLACK_TUPLE, 250, 50)
        load_list_characters(game_context.get_sprites())

        selected_character = handle_events()
        # Si el usuario quiere cerrar la ventana
        if selected_character == "QUIT":
            running = False
        elif selected_character is not None:
            return selected_character

        pygame.display.update()

    pygame.quit()
