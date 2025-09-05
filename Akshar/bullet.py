import pygame
from main import BULLET_SPEED, YELLOW


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 12), pygame.SRCALPHA)
        pygame.draw.rect(self.image, YELLOW, (0, 0, 4, 12))
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, -BULLET_SPEED)

    def update(self, dt):
        self.pos += self.velocity * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if self.rect.bottom < -10:
            self.kill()
