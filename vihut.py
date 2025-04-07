import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_path, size, speed, score_value):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(x=pygame.display.get_surface().get_width(),
                                        y=random.randint(0, pygame.display.get_surface().get_height() - size))
        self.speed_x = speed
        self.size = size
        self.score_value = score_value

    def update(self):
        self.rect.x -= self.speed_x
        if self.rect.right < 0:
            self.kill()

class Background:
    def __init__(self):
        screen = pygame.display.get_surface()
        self.stars = [
            pygame.Rect(
                random.randint(0, screen.get_width()),
                random.randint(0, screen.get_height()),
                random.randint(1, 3),
                random.randint(1, 3)
            ) for _ in range(200)
        ]
        self.speed = 1

    def update(self):
        screen = pygame.display.get_surface()
        for star in self.stars:
            star.x -= self.speed
            if star.x < 0:
                star.x = screen.get_width()
                star.y = random.randint(0, screen.get_height())

    def draw(self):
        screen = pygame.display.get_surface()
        for star in self.stars:
            pygame.draw.rect(screen, (255, 255, 255), star)
