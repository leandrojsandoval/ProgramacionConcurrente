import constants, pygame

DEFAULT_BORDER_SIZE = 2


class Button:

    def __init__(
        self,
        text,
        x,
        y,
        width,
        height,
        color,
        hover_color=None,
        border_color=None,
        border_size=None,
        font=None,
    ):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.border_color = border_color
        # Si se especifica border_color, se asigna el border_size, de lo contrario se establece como None
        self.border_size = border_size if border_color is None else DEFAULT_BORDER_SIZE
        self.font = font if font else pygame.font.Font(None)

    def draw(self, window, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if self.hover_color:
                color = self.hover_color
            else:
                color = self.color
        else:
            color = self.color

        pygame.draw.rect(window, color, self.rect)

        if self.border_color is not None:
            pygame.draw.rect(window, self.border_color, self.rect,
                             self.border_size)

        text_surface = self.font.render(self.text, True,
                                        constants.COLOR_WHITE_TUPLE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        window.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
