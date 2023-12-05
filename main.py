import pygame
from pygame import sprite, transform, key, image

class Car(sprite.Sprite):
    def __init__(self, image_path, x, y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(image_path), (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, paredes):
        keys = key.get_pressed()
        original_rect = self.rect.copy()
        
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
            if self.check_collision(paredes):
                self.rect = original_rect

        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
            if self.check_collision(paredes):
                self.rect = original_rect

        if keys[pygame.K_UP]:
            self.rect.y -= 5
            if self.check_collision(paredes):
                self.rect = original_rect

        if keys[pygame.K_DOWN]:
            self.rect.y += 5
            if self.check_collision(paredes):
                self.rect = original_rect

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

# Ejemplo de uso
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

car_image_path = "globy.png"
car = Car(car_image_path, 100, 100)
pared1 = Pared(100, 300, 50, 200)
pared2 = Pared(200, 100, 50, 200)

all_sprites = pygame.sprite.Group()
all_sprites.add(car)

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

    screen.fill((255, 255, 255))
    for pared in paredes:
        pared.dibujar()
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(100)

pygame.quit()
