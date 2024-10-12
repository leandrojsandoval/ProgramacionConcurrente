import pygame
import constants

class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
            cls._window = pygame.display.set_mode((constants.INITIAL_WIDTH, constants.INITIAL_HEIGHT), pygame.RESIZABLE)  # Modo ventana y resizable
            pygame.display.set_caption("Combate por Turnos Estilo Pokémon")
        return cls._instance

    @property
    def window(self):
        return self._window
