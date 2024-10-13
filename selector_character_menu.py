import constants, game_context, pygame, utils

# =========================================== Variables ===========================================

bg_image = pygame.image.load("assets/background_waterfalls.jpg")
characters = game_context.get_characters()
current_selection = 0
first_visible_index = 0  # Índice del primer personaje visible
visible_characters_count = 5  # Número de personajes visibles en la pantalla
window = game_context.get_window()

# =========================================== Sprite ===========================================


def load_list_characters(sprites):
    for i in range(
            first_visible_index,
            min(first_visible_index + visible_characters_count,
                len(characters)),
    ):
        character = list(characters.values())[i]
        utils.draw_text(character.name, 40, 250,
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
        scaled_image = pygame.transform.scale(image_to_draw, (180, 180))
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
                current_selection = (current_selection + direction
                                    ) % total_characters  # Movimiento circular

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
    running = True
    while running:
        window.fill(constants.COLOR_WHITE_TUPLE)
        window.blit(bg_image, (0, 0))
        utils.draw_text("Elige tu Personaje", 60, 250, 50)
        load_list_characters(game_context.get_sprites())

        selected_character = handle_events()
        # Si el usuario quiere cerrar la ventana
        if selected_character == "QUIT":
            running = False
        elif selected_character is not None:
            return selected_character

        pygame.display.update()

    pygame.quit()
