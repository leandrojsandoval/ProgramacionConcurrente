import pygame

class Boton:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)  # Mantén esto como antes
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.Font(None, 36)

    def draw(self, window, mouse_pos):
        # Cambia el color del botón si el mouse está sobre él
        if self.rect.collidepoint(mouse_pos):
            color = self.hover_color
        else:
            color = self.color

        # Dibuja el botón
        pygame.draw.rect(window, color, self.rect)

        # Dibuja el contorno del botón
        pygame.draw.rect(window, (0, 0, 0), self.rect, 2)  # Contorno negro con un grosor de 2 píxeles

        # Dibuja el texto en el botón
        text_surface = self.font.render(self.text, True, (255, 255, 255))  # Texto blanco
        text_rect = text_surface.get_rect(center=self.rect.center)
        window.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
