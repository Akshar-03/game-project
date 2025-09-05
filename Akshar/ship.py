import pygame
from bullet import Bullet
from main import WIDTH, HEIGHT, SHIP_SPEED, BOOST_MULTIPLIER, MAX_AMMO, RELOAD_TIME
from main import WHITE, GRAY


def clamp(val, a, b):
    return max(a, min(b, val))


class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.Surface((40, 48), pygame.SRCALPHA)
        self._draw_ship(self.original_image)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.last_shot = 0
        self.ammo = MAX_AMMO
        self.reloading = False
        self.reload_start = 0

    def _draw_ship(self, surf):
        w, h = surf.get_size()
        pygame.draw.polygon(surf, WHITE, [(w/2, 2), (w-4, h-10), (w/2, h-6)])
        pygame.draw.polygon(surf, GRAY, [(w/2, 2), (4, h-10), (w/2, h-6)])
        pygame.draw.circle(surf, (30, 100, 220), (int(w*0.62), int(h*0.38)), 6)

    def update(self, dt, keys, boosting):
        if self.reloading:
            if pygame.time.get_ticks() - self.reload_start >= RELOAD_TIME:
                self.ammo = MAX_AMMO
                self.reloading = False

        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1

        dir_vec = pygame.math.Vector2(dx, dy)
        if dir_vec.length_squared() > 0:
            dir_vec = dir_vec.normalize()

        speed = SHIP_SPEED * (BOOST_MULTIPLIER if boosting else 1.0)
        self.velocity = dir_vec * speed
        self.pos += self.velocity * dt

        self.pos.x = clamp(self.pos.x, 20, WIDTH - 20)
        self.pos.y = clamp(self.pos.y, 20, HEIGHT - 20)
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def can_shoot(self):
        now = pygame.time.get_ticks()
        return not self.reloading and self.ammo > 0 and (now - self.last_shot >= 200)

    def shoot(self):
        self.last_shot = pygame.time.get_ticks()
        self.ammo -= 1
        if self.ammo <= 0:
            self.reloading = True
            self.reload_start = pygame.time.get_ticks()
        return Bullet(self.rect.centerx, self.rect.top - 6)
