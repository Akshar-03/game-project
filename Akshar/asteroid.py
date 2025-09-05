import pygame, math, random
from main import WIDTH, HEIGHT, GRAY


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, size, speed, angle_variation=30):
        super().__init__()
        self.size = size
        self.image = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        self._draw_asteroid(self.image, size)
        self.rect = self.image.get_rect(center=(x, -size))
        self.pos = pygame.math.Vector2(self.rect.center)
        angle = 90 + random.uniform(-angle_variation, angle_variation)
        rad = math.radians(angle)
        self.velocity = pygame.math.Vector2(math.cos(rad), math.sin(rad)) * speed
        self.rot = 0
        self.rot_speed = random.uniform(-90, 90)

    def _draw_asteroid(self, surf, r):
        cx, cy = surf.get_width() // 2, surf.get_height() // 2
        points = []
        spikes = max(6, int(r/4))
        for i in range(spikes):
            ang = i * (2*math.pi/spikes)
            radius = r * random.uniform(0.75, 1.2)
            x = cx + math.cos(ang) * radius
            y = cy + math.sin(ang) * radius
            points.append((x, y))
        pygame.draw.polygon(surf, GRAY, points)
        pygame.draw.polygon(surf, (120, 120, 120), points, 2)

    def update(self, dt):
        self.pos += self.velocity * dt
        self.rot = (self.rot + self.rot_speed * dt) % 360
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if self.rect.top > HEIGHT + 60 or self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()
