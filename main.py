import pygame
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("The Waiting room v1.0")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Configuración del personaje
TAMANO_PERSONAJE = 40
personaje = pygame.Rect(ANCHO//2, ALTO//2, TAMANO_PERSONAJE, TAMANO_PERSONAJE)
VELOCIDAD = 5
puntos = 0

# Configuración de los enemigos
enemigos = [pygame.Rect(random.randint(0, ANCHO-30), random.randint(0, ALTO-30), 30, 30) for _ in range(5)]

# Configuración de los objetos especiales
objetos_especiales = []

# Rectángulo central
rectangulo_central = pygame.Rect(ANCHO//3, ALTO//3, ANCHO//3, ALTO//3)

# Configuración de los disparos
disparos = []
TIEMPO_VIDA_DISPARO = 2000  # en milisegundos
#sonido_disparo = pygame.mixer.Sound("disparo.wav")

# Bucle del juego
reloj = pygame.time.Clock()
corriendo = True
while corriendo:
    reloj.tick(60)
    VENTANA.fill(BLANCO)
    
    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            disparos.append((pygame.time.get_ticks(), personaje.x, personaje.y))
            sonido_disparo.play()
    
    # Movimiento del personaje
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w]: personaje.y -= VELOCIDAD
    if teclas[pygame.K_s]: personaje.y += VELOCIDAD
    if teclas[pygame.K_a]: personaje.x -= VELOCIDAD
    if teclas[pygame.K_d]: personaje.x += VELOCIDAD
    
    # Colisiones con enemigos
    for enemigo in enemigos[:]:
        if personaje.colliderect(enemigo):
            enemigos.remove(enemigo)
            puntos += 1
    
    # Aparición de objetos especiales aleatoriamente
    if random.randint(1, 200) == 1:
        objetos_especiales.append(pygame.Rect(random.randint(0, ANCHO-20), random.randint(0, ALTO-20), 20, 20))
    
    # Colisión con objetos especiales
    for objeto in objetos_especiales[:]:
        if personaje.colliderect(objeto):
            objetos_especiales.remove(objeto)
            puntos += 50
    
    # Colisión con el rectángulo central y los bordes
    if personaje.colliderect(rectangulo_central) or personaje.left < 0 or personaje.right > ANCHO or personaje.top < 0 or personaje.bottom > ALTO:
        puntos -= 5
    
    # Dibujar elementos
    pygame.draw.rect(VENTANA, AZUL, personaje)
    for enemigo in enemigos:
        pygame.draw.rect(VENTANA, ROJO, enemigo)
    for objeto in objetos_especiales:
        pygame.draw.rect(VENTANA, VERDE, objeto)
    pygame.draw.rect(VENTANA, NEGRO, rectangulo_central, 2)
    
    # Dibujar y eliminar disparos después de su tiempo de vida
    tiempo_actual = pygame.time.get_ticks()
    for disparo in disparos[:]:
        if tiempo_actual - disparo[0] > TIEMPO_VIDA_DISPARO:
            disparos.remove(disparo)
        else:
            pygame.draw.circle(VENTANA, NEGRO, (disparo[1], disparo[2]), 5)
    
    # Mostrar puntaje
    fuente = pygame.font.Font(None, 36)
    texto_puntos = fuente.render(f"Puntos: {puntos}", True, NEGRO)
    VENTANA.blit(texto_puntos, (10, 10))
    
    pygame.display.update()

pygame.quit()
