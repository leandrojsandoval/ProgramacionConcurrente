import game_context

window = game_context.get_window()

class Text:
    def __init__(self, content, font, size, color, x_position, y_position):
        self.content = content
        self.font = font
        self.size = size
        self.color = color
        self.x_position = x_position
        self.y_position = y_position
