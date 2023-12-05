import pygame
from pygame import sprite, transform, key, image

class Personajes(sprite.Sprite):
    def __init__(self, image_path, x, y, controlable=True):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(image_path), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.controlable = controlable

    def update(self, paredes):
        if self.controlable:
            keys = key.get_pressed()
            
            movimiento_x = 0
            movimiento_y = 0
            
            if keys[pygame.K_LEFT] and self.rect.x > 0:
                movimiento_x -= 5
            if keys[pygame.K_RIGHT] and self.rect.x < screen.get_width() - self.rect.width:
                movimiento_x += 5
            if keys[pygame.K_UP] and self.rect.y > 0:
                movimiento_y -= 5
            if keys[pygame.K_DOWN] and self.rect.y < screen.get_height() - self.rect.height:
                movimiento_y += 5

            position_x = self.rect.x
            self.rect.x += movimiento_x
            if self.check_collision(paredes):
                self.rect.x = position_x

            position_y = self.rect.y
            self.rect.y += movimiento_y
            if self.check_collision(paredes):
                self.rect.y = position_y

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

class Enemigo(Personajes):
    def __init__(self, image_path, x, y, punto_inicial, punto_final, movimiento):
        super().__init__(image_path, x, y, controlable=False)
        self.punto_inicial = punto_inicial
        self.punto_final = punto_final
        self.velocidad = 2
        self.movimiento = movimiento

    def mover_verticalmente(self):
        self.rect.y += self.velocidad
        if self.rect.y <= self.punto_inicial or self.rect.y >= self.punto_final:
            self.velocidad *= -1

    def mover_horizontalmente(self):
        self.rect.x += self.velocidad
        if self.rect.x <= self.punto_inicial or self.rect.x >= self.punto_final:
            self.velocidad *= -1

    def update(self, _):
        if self.movimiento == 'vertical':
            self.mover_verticalmente()
        elif self.movimiento == 'horizontal':
            self.mover_horizontalmente()

def mostrar_pantalla_perdida():
    pantalla_perdida = transform.scale(image.load(loss_image_path), (800, 600))
    screen.blit(pantalla_perdida, (0, 0))
    pygame.display.flip()
    pygame.time.wait(3000)



pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

car_image_path = "pac-1.png"
enemies_image_path = "hero.png"
loss_image_path = "game-over_1.png"

car = Personajes(car_image_path, 100, 100, controlable=True)
enemigo1 = Enemigo(enemies_image_path, 400, 400, 300, 500, movimiento='horizontal')
enemigo2 = Enemigo("cyborg.png", 400, 300, 300, 400, movimiento='vertical')

pared1 = Pared(100, 300, 50, 200)
pared2 = Pared(200, 100, 50, 200)

all_sprites = pygame.sprite.Group()
all_sprites.add(car)
all_sprites.add(enemigo1)
all_sprites.add(enemigo2)

paredes = [pared1, pared2]


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