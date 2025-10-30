import pygame
import math
import numpy as np

# Inicializar Pygame
pygame.init()

# Configuración de la ventana 
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Movimiento del objeto con fuerzas")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)

# Parámetros del problema
t_max = 10.0  # Tiempo total (s)
dt = 0.05  # Intervalo de tiempo (s)
num_frames = int(t_max / dt)

# Escala para convertir metros a píxeles
SCALE = 50  # píxeles por metro
OFFSET_X, OFFSET_Y = 2 * SCALE, HEIGHT - 50  

# Fuerzas (en N)
# F1_x, F1_y = -0.6, -5.5  # Fuerza 1
F1_x, F1_y = 3, 0
F2_x, F2_y = 0, -4.5     # Fuerza 2
F_net_x, F_net_y = F1_x + F2_x, F1_y + F2_y  # Fuerza neta
F_net_magnitude = math.sqrt(F_net_x**2 + F_net_y**2)  # Magnitud de la fuerza neta

# Calcular la masa y la aceleración a partir de F_net (ajustada)
a_magnitude_initial = math.sqrt(0.5**2 + 0**2)  # Magnitud inicial de a (para consistencia)
mass = F_net_magnitude / a_magnitude_initial    # m = |F_net| / |a_initial|
a_x = F_net_x / mass                            # a_x = F_net_x / m
a_y = F_net_y / mass                            # a_y = F_net_y / m

# Calcular posiciones y tiempo
t = np.linspace(0, t_max, num_frames)
x = 0.5 * a_x * t**2  # x(t) = (1/2) * a_x * t^2 (usando a_x de F_net)
y = 0.5 * a_y * t**2  # y(t) = (1/2) * a_y * t^2 (usando a_y de F_net)

# Índice del frame
frame = 0

# Calculo de las preguntas

# a) Dirección de la aceleración (basada en F_net)
a_magnitude = math.sqrt(a_x**2 + a_y**2) 
angle_acc = math.atan2(a_y, a_x) 
angle_deg = math.degrees(angle_acc)  
direction_acc = angle_deg if angle_deg >= 0 else 360 + angle_deg  # Corrección del ajuste

# b) Masa del objeto
mass = F_net_magnitude / a_magnitude_initial  # Usamos la magnitud inicial para consistencia

# c) Rapidez después de 10.0 s (objeto en reposo inicialmente)
v_x = a_x * 10.0  
v_y = a_y * 10.0 
speed = math.sqrt(v_x**2 + v_y**2) 

# d) Componentes de velocidad después de 10.0 s
v_x_comp = v_x
v_y_comp = v_y

# Imprimir resultados en la terminal
print(f"a) Direccion de la aceleracion: {direction_acc:.2f} grados")
print(f"b) Masa del objeto: {mass:.3f} kg ")
print(f"c) Rapidez despues de 10.0 s: {speed:.2f} m/s")
print(f"d) Componentes de velocidad despues de 10.0 s: \n Velocidad en X = {v_x_comp:.2f} m/s, \n Velocidad en Y = {v_y_comp:.2f} m/s")

# Bucle principal
running = True
clock = pygame.time.Clock()

def rotate_point(point, angle, center):
    x, y = point[0] - center[0], point[1] - center[1]
    new_x = x * math.cos(angle) - y * math.sin(angle) + center[0]
    new_y = x * math.sin(angle) + y * math.cos(angle) + center[1]
    return (new_x, new_y)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limpiar pantalla con fondo blanco
    screen.fill(WHITE)

    # Convertir coordenadas (y-axis invertido en Pygame)
    screen_x = x[frame] * SCALE + OFFSET_X
    screen_y = HEIGHT - (y[frame] * SCALE + OFFSET_Y)  # Invertir eje y

    # Dibujar rectángulo
    rect_width, rect_height = 2 * SCALE, 1 * SCALE
    rect = pygame.Rect(screen_x - rect_width // 2, screen_y - rect_height // 2, rect_width, rect_height)
    pygame.draw.rect(screen, RED, rect) 

    # Dibujar flechas de fuerzas desde el centro del rectángulo
    center_x, center_y = screen_x, screen_y

    # Flecha F1
    end_x1 = center_x + F1_x * SCALE / 5 * 4  
    end_y1 = center_y - F1_y * SCALE / 5 * 4  # Invertir y
    pygame.draw.line(screen, BLUE, (center_x, center_y), (end_x1, end_y1), 3)
    # Calcular ángulo de la flecha
    angle1 = math.atan2(F1_y, F1_x)  # Ángulo en radianes
    arrow_head1 = [
        (end_x1, end_y1),
        rotate_point((end_x1 - 5, end_y1 + 5), -angle1, (end_x1, end_y1)), 
        rotate_point((end_x1 + 5, end_y1 + 5), -angle1, (end_x1, end_y1))
    ]
    pygame.draw.polygon(screen, BLUE, arrow_head1)

    # Flecha F2
    end_x2 = center_x + F2_x * SCALE / 5 * 4
    end_y2 = center_y - F2_y * SCALE / 5 * 4
    pygame.draw.line(screen, GREEN, (center_x, center_y), (end_x2, end_y2), 3)
    # Calcular ángulo de la flecha
    angle2 = math.atan2(F2_y, F2_x)
    arrow_head2 = [
        (end_x2, end_y2),
        rotate_point((end_x2 - 5, end_y2 + 5), -angle2, (end_x2, end_y2)),
        rotate_point((end_x2 + 5, end_y2 + 5), -angle2, (end_x2, end_y2))
    ]
    pygame.draw.polygon(screen, GREEN, arrow_head2)

    # Flecha F_net
    end_x_net = center_x + F_net_x * SCALE / 5 * 4
    end_y_net = center_y - F_net_y * SCALE / 5 * 4
    pygame.draw.line(screen, PURPLE, (center_x, center_y), (end_x_net, end_y_net), 3)
    # Calcular ángulo de la flecha
    angle_net = math.atan2(F_net_y, F_net_x)
    arrow_head_net = [
        (end_x_net, end_y_net),
        rotate_point((end_x_net - 5, end_y_net + 5), -angle_net, (end_x_net, end_y_net)),
        rotate_point((end_x_net + 5, end_y_net + 5), -angle_net, (end_x_net, end_y_net))
    ]
    pygame.draw.polygon(screen, PURPLE, arrow_head_net)

    # Actualizar frame
    frame = (frame + 1) % num_frames
    if frame == 0:
        print("Animacion reiniciada")

    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

# Cerrar Pygame
pygame.quit()