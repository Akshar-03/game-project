import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, max_radius=36, duration=400):
        super().__init__()
        self.x = x
        self.y = y
        self.max_radius = max_radius
        self.duration = duration
        self.start = pygame.time.get_ticks()
        self.image = pygame.Surface((max_radius*2+4, max_radius*2+4), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, dt):
        now = pygame.time.get_ticks()
        t = (now - self.start) / self.duration
        if t >= 1.0:
            self.kill()
            return
        radius = int(self.max_radius * t)
        alpha = int(255 * (1 - t))
        surf = pygame.Surface((self.max_radius*2+4, self.max_radius*2+4), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 180, 60, alpha), (self.max_radius+2, self.max_radius+2), radius)
        self.image = surf
        self.rect = self.image.get_rect(center=(self.x, self.y))
