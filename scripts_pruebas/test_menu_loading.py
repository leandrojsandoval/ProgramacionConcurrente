import pygame
import time
import threading

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Dynamic Loading Bar Example")

# Definir colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Fuente para el texto de carga
font = pygame.font.Font(None, 36)

# Definir las dimensiones de la barra de progreso
BAR_WIDTH = 400
BAR_HEIGHT = 30
bar_x = (800 - BAR_WIDTH) // 2
bar_y = (600 - BAR_HEIGHT) // 2

# Variable para almacenar los recursos cargados
loaded_resources = {}

# Variable para el progreso de la barra (0 a 100%)
progress = 0

# Función para cargar recursos (simulación con tiempo de espera)
def load_resources():
    global progress
    resources = ['image', 'sound', 'level_data']
    total_resources = len(resources)

    for i, resource in enumerate(resources):
        time.sleep(1)  # Simular el tiempo de carga
        loaded_resources[resource] = f"{resource} cargado"
        
        # Incremento grande por cada recurso cargado
        progress += 25  # Simular un aumento del 25% por recurso cargado
        progress = min(progress, 100)  # Asegurarse de que no pase del 100%

# Función para mostrar la pantalla de carga con barra de progreso
def show_loading_screen():
    global progress
    clock = pygame.time.Clock()

    while progress < 100:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Limpiar la pantalla
        screen.fill(BLACK)

        # Dibujar la barra de progreso
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, BAR_WIDTH, BAR_HEIGHT), 2)  # Marco de la barra
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, int(BAR_WIDTH * progress / 100), BAR_HEIGHT))  # Barra de progreso

        # Mostrar el porcentaje de carga
        loading_text = font.render(f"Cargando... {int(progress)}%", True, WHITE)
        screen.blit(loading_text, (bar_x + 50, bar_y - 40))

        # Simular pequeños incrementos en el progreso para hacerlo más dinámico
        if progress < 100:
            progress += 0.2  # Incrementar poco a poco
            progress = min(progress, 100)  # Asegurarse de que no pase del 100%

        # Actualizar la pantalla
        pygame.display.flip()
        clock.tick(60)  # Controlar la velocidad de la animación

# Iniciar un hilo para cargar recursos en segundo plano
loading_thread = threading.Thread(target=load_resources)
loading_thread.start()

# Mostrar la pantalla de carga mientras los recursos se cargan
show_loading_screen()

# Finaliza el hilo una vez que la carga ha terminado
loading_thread.join()

# Una vez que los recursos se han cargado, mostrar la pantalla principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limpiar pantalla
    screen.fill(WHITE)

    # Usar los recursos cargados (en este ejemplo, solo mostramos el texto de que fueron cargados)
    for i, resource in enumerate(loaded_resources):
        resource_text = font.render(f"{resource}: {loaded_resources[resource]}", True, BLACK)
        screen.blit(resource_text, (50, 50 + i * 40))

    # Actualizar la pantalla
    pygame.display.flip()

# Cerrar Pygame
pygame.quit()
