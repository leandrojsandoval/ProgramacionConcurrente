import constants, game_context, os, pygame

class BackgroundAnimated:
    def __init__(self, path, base_name, frame_delay):
        self.window = game_context.get_window()  # Asignar self.window en el constructor
        self.frames = self.load_animation_frames(path, base_name)
        self.current_frame = 0
        self.frame_counter = 0
        self.frame_delay = frame_delay

    def update(self):
        # Actualiza el cuadro de animación y el contador
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.frame_counter = 0
        return self.frames[self.current_frame]

    def reset(self):
        self.current_frame = 0
        self.frame_counter = 0

    def load_animation_frames(self, path_frames, frame_base_name):
        frames = []
        all_files = os.listdir(path_frames)
        for file_name in all_files:
            if file_name.startswith(frame_base_name) and file_name.endswith(constants.EXTENSION_PNG):
                frame_path = os.path.join(path_frames, file_name)
                frame_image = pygame.image.load(frame_path)
                # Escalar las imágenes al tamaño de la ventana actual
                frame_image = pygame.transform.scale(frame_image, (self.window.get_width(), self.window.get_height()))
                frames.append(frame_image)
        return frames

    def draw_background(self):
        # Dibujar el frame actual en la ventana
        self.window.blit(self.frames[self.current_frame], (0, 0))
