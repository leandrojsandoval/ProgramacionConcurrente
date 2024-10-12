# main.py
import pygame
from boton import Boton  # Asegúrate de que el archivo boton.py esté en el mismo directorio

# Inicialización de Pygame
pygame.init()

# Dimensiones iniciales de la ventana
INITIAL_WIDTH = 800
INITIAL_HEIGHT = 600
WINDOW = pygame.display.set_mode((INITIAL_WIDTH, INITIAL_HEIGHT), pygame.RESIZABLE)  # Modo ventana y resizable
pygame.display.set_caption("Combate por Turnos Estilo Pokémon")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Tamaño de los botones
BUTTON_SPACING = 20  # Espacio entre botones
TOTAL_BUTTONS = 4  # Número total de botones
BUTTON_WIDTH = 150  # Ancho deseado de los botones

def create_buttons():
    """Crea los botones con posiciones iniciales."""
    buttons = [
        Boton("Atacar", 0, 0, BUTTON_WIDTH, 0, (100, 200, 100), (150, 250, 150)),
        Boton("Defender", 0, 0, BUTTON_WIDTH, 0, (100, 200, 100), (150, 250, 150)),
        Boton("Descansar", 0, 0, BUTTON_WIDTH, 0, (100, 200, 100), (150, 250, 150)),
        Boton("Concentrarse", 0, 0, BUTTON_WIDTH, 0, (100, 200, 100), (150, 250, 150))
    ]
    return buttons

def main():
    global WINDOW  # Declarar WINDOW como global
    running = True
    width, height = INITIAL_WIDTH, INITIAL_HEIGHT  # Dimensiones iniciales

    # Crear botones
    buttons = create_buttons()

    # Actualizar la posición inicial de los botones
    for index, button in enumerate(buttons):
        button.update_position(width, height, index, TOTAL_BUTTONS, BUTTON_SPACING)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Verificar qué botón ha sido clickeado
                for button in buttons:
                    if button.is_clicked(mouse_pos):
                        print(f"Has elegido {button.text}!")

            # Manejar el evento de redimensionar la ventana
            if event.type == pygame.VIDEORESIZE:
                # Actualiza el tamaño de la ventana
                width, height = event.w, event.h
                WINDOW = pygame.display.set_mode((width, height), pygame.RESIZABLE)  # Asegúrate de que se mantenga resizable

                # Actualizar posiciones y tamaños de los botones
                for index, button in enumerate(buttons):
                    button.update_position(width, height, index, TOTAL_BUTTONS, BUTTON_SPACING)

        # Dibujar la ventana
        WINDOW.fill(WHITE)

        # Obtener la posición del mouse
        mouse_pos = pygame.mouse.get_pos()

        # Dibujar botones
        for button in buttons:
            button.draw(WINDOW, mouse_pos)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
