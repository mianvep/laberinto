import pygame
from pygame import sprite, transform, key, image

class Car(sprite.Sprite):
    def __init__(self, image_path, x, y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(image_path), (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def check_collision(self, paredes):
        for pared in paredes:
            if self.rect.colliderect(pared.rect):
                return True
        return False

class Pared:
    def __init__(self, x, y, ancho, alto):
        self.rect = pygame.Rect(x, y, ancho, alto)

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, (0, 0, 0), self.rect)

# Inicialización de Pygame y configuración de la pantalla
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Carga de imágenes y creación de objetos
car_image_path = "globy.png"
background_derrota_path = "youloss.png"  
fondo_derrota = pygame.image.load(background_derrota_path)
fondo_derrota = pygame.transform.scale(fondo_derrota, (800, 600))
car = Car(car_image_path, 100, 100)
pared1 = Pared(100, 300, 50, 200)
pared2 = Pared(200, 100, 50, 200)

paredes = [pared1, pared2]
modo_derrota = False

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                running = False

    keys = key.get_pressed()
    if not modo_derrota:
        movimiento_x = 0
        movimiento_y = 0
        
        if keys[pygame.K_LEFT]:
            movimiento_x -= 5
        if keys[pygame.K_RIGHT]:
            movimiento_x += 5
        if keys[pygame.K_UP]:
            movimiento_y -= 5
        if keys[pygame.K_DOWN]:
            movimiento_y += 5

        car.rect.x += movimiento_x
        car.rect.y += movimiento_y

        if car.check_collision(paredes):
            modo_derrota = True

    if modo_derrota:
        screen.blit(fondo_derrota, (0, 0))
    else:
        screen.fill((255, 255, 255))
        for pared in paredes:
            pared.dibujar(screen)
        screen.blit(car.image, car.rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
