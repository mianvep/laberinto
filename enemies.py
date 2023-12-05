import pygame
from pygame import sprite, transform, key, image

class Car(sprite.Sprite):
    def __init__(self, image_path, x, y, controlable=True):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(image_path), (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.controlable = controlable

    def update(self, paredes):
        if self.controlable:
            keys = key.get_pressed()
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

            original_x = self.rect.x
            self.rect.x += movimiento_x
            if self.check_collision(paredes):
                self.rect.x = original_x

            original_y = self.rect.y
            self.rect.y += movimiento_y
            if self.check_collision(paredes):
                self.rect.y = original_y

    def check_collision(self, paredes):
        for pared in paredes:
            if self.rect.colliderect(pared.rect):
                return True
        return False

class Pared:
    def __init__(self, x, y, ancho, alto):
        self.rect = pygame.Rect(x, y, ancho, alto)

    def dibujar(self):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)

class Enemigo(Car):
    def __init__(self, image_path, x, y, min_val, max_val, movimiento='horizontal'):
        super().__init__(image_path, x, y, controlable=False)
        self.min_val = min_val
        self.max_val = max_val
        self.velocidad = 2
        self.movimiento = movimiento

    def mover_horizontalmente(self):
        self.rect.x += self.velocidad
        if self.rect.x <= self.min_val or self.rect.x >= self.max_val:
            self.velocidad *= -1

    def mover_verticalmente(self):
        self.rect.y += self.velocidad
        if self.rect.y <= self.min_val or self.rect.y >= self.max_val:
            self.velocidad *= -1

    def update(self, _):
        if self.movimiento == 'horizontal':
            self.mover_horizontalmente()
        elif self.movimiento == 'vertical':
            self.mover_verticalmente()

def mostrar_pantalla_perdida():
    pantalla_perdida = transform.scale(image.load(loss_image_path), (800, 600))
    screen.blit(pantalla_perdida, (0, 0))
    pygame.display.flip()
    pygame.time.wait(3000)

# Configuración inicial
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

car_image_path = "globy.png"
enemies_image_path = "hero.png"
loss_image_path = "youloss.png"
car = Car(car_image_path, 100, 100, controlable=True)
enemigo1 = Enemigo(enemies_image_path, 400, 400, 300, 500, movimiento='horizontal')
enemigo2 = Enemigo("hero.png", 200, 200, 100, 500, movimiento='vertical')

pared1 = Pared(100, 300, 50, 200)
pared2 = Pared(200, 100, 50, 200)

all_sprites = pygame.sprite.Group()
all_sprites.add(car)
all_sprites.add(enemigo1)
all_sprites.add(enemigo2)

paredes = [pared1, pared2]

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                running = False

    all_sprites.update(paredes)

    if car.rect.colliderect(enemigo1.rect) or car.rect.colliderect(enemigo2.rect):
        mostrar_pantalla_perdida()
        running = False
        continue

    screen.fill((255, 255, 255))
    for pared in paredes:
        pared.dibujar()
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(100)

pygame.quit()
