import pygame

class Boton:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.Font(None, 40)

    def draw(self, window, mouse_pos):
        # Cambiar el color si el mouse está sobre el botón
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        
        # Dibujar el borde negro del botón
        border_rect = self.rect.inflate(10, 10)  # Aumentar el tamaño del rectángulo para el borde
        pygame.draw.rect(window, (0, 0, 0), border_rect)  # Dibuja el borde en negro
        
        # Dibujar el botón
        pygame.draw.rect(window, color, self.rect)

        # Dibujar el texto del botón
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        window.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def update_position(self, screen_width, screen_height, button_index, total_buttons, button_spacing):
        """Actualiza la posición y tamaño del botón en función del tamaño de la ventana."""
        button_width_scaled = (screen_width - button_spacing * (total_buttons - 1)) // total_buttons
        button_height_scaled = screen_height // 12  # Ajustar según tus necesidades

        # Calcular la posición centrada horizontalmente
        button_x = (screen_width - (button_width_scaled * total_buttons + button_spacing * (total_buttons - 1))) // 2
        button_y = screen_height - button_height_scaled - 20  # Colocar los botones en la parte inferior con un margen de 20

        # Actualizar la posición del botón
        self.rect.x = button_x + button_index * (button_width_scaled + button_spacing)
        self.rect.y = button_y
        # Actualizar el tamaño del botón
        self.rect.width = button_width_scaled
        self.rect.height = button_height_scaled
