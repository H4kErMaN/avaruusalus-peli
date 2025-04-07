import pygame
import random

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen_height):
        super().__init__()
        self.image = pygame.image.load("alus.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (100, screen_height // 2)
        self.speed_y = 0

    def update(self):
        self.rect.y += self.speed_y
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(pygame.display.get_surface().get_height(), self.rect.bottom)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = 10

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.left > pygame.display.get_surface().get_width():
            self.kill()
