import pygame, random, math
from collections import deque
from ship import Ship
from asteroid import Asteroid
from explosion import Explosion

# constants
WIDTH, HEIGHT = 800, 600
FPS = 60
ASTEROID_SPAWN_EVENT = pygame.USEREVENT + 1
ASTEROID_SPAWN_INTERVAL_MS = 700

SHIP_SPEED = 250
BOOST_MULTIPLIER = 2.2
BULLET_SPEED = 600
ASTEROID_MIN_SPEED = 80
ASTEROID_MAX_SPEED = 220
ASTEROID_MIN_SIZE = 18
ASTEROID_MAX_SIZE = 54
BULLET_COOLDOWN = 200
MAX_LIVES = 3
MAX_AMMO = 20
RELOAD_TIME = 4000

WHITE = (255, 255, 255)
GRAY = (160, 160, 160)
BLACK = (0, 0, 0)
YELLOW = (255, 220, 60)
RED = (220, 30, 30)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rocket — Space Run")
    clock = pygame.time.Clock()

    stars = [[random.randrange(0, WIDTH), random.randrange(0, HEIGHT), random.uniform(10, 120)] for _ in range(120)]

    ship = Ship(WIDTH//2, HEIGHT - 100)
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    all_sprites.add(ship)

    score = 0
    lives = MAX_LIVES
    running = True
    paused = False

    pygame.time.set_timer(ASTEROID_SPAWN_EVENT, ASTEROID_SPAWN_INTERVAL_MS)

    font = pygame.font.Font(None, 28)
    bigfont = pygame.font.Font(None, 64)

    highscores = deque(maxlen=5)

    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_p:
                    paused = not paused
            elif event.type == ASTEROID_SPAWN_EVENT and not paused:
                x = random.uniform(20, WIDTH-20)
                size = random.randint(ASTEROID_MIN_SIZE, ASTEROID_MAX_SIZE)
                speed = random.uniform(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)
                a = Asteroid(x, size, speed)
                asteroids.add(a)
                all_sprites.add(a)

        if paused:
            screen.fill(BLACK)
            draw_starfield(screen, stars, 0)
            text = bigfont.render("PAUSED", True, WHITE)
            screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))
            pygame.display.flip()
            continue

        keys = pygame.key.get_pressed()
        boosting = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

        if keys[pygame.K_SPACE] and ship.can_shoot():
            b = ship.shoot()
            bullets.add(b)
            all_sprites.add(b)

        ship.update(dt, keys, boosting)
        bullets.update(dt)
        asteroids.update(dt)
        explosions.update(dt)

        hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
        for a in hits:
            score += int(a.size * 10 / 4)
            exp = Explosion(a.rect.centerx, a.rect.centery, max_radius=int(a.size*0.8))
            explosions.add(exp)
            all_sprites.add(exp)

        ship_hits = pygame.sprite.spritecollide(ship, asteroids, True)
        for a in ship_hits:
            lives -= 1
            exp = Explosion(a.rect.centerx, a.rect.centery, max_radius=int(a.size*1.2))
            explosions.add(exp)
            all_sprites.add(exp)
            if lives <= 0:
                highscores.appendleft(score)
                game_over(screen, score, font, bigfont, highscores)
                score = 0
                lives = MAX_LIVES
                for s in asteroids: s.kill()
                for s in bullets: s.kill()
                for s in explosions: s.kill()
                ship.pos = pygame.math.Vector2(WIDTH//2, HEIGHT-100)
                ship.ammo = MAX_AMMO
                ship.reloading = False

        screen.fill(BLACK)
        draw_starfield(screen, stars, dt)

        if boosting:
            draw_boost_trail(screen, ship)

        for sprite in all_sprites:
            if isinstance(sprite, Asteroid):
                rotated = pygame.transform.rotozoom(sprite.image, sprite.rot, 1.0)
                rect = rotated.get_rect(center=sprite.rect.center)
                screen.blit(rotated, rect)
            else:
                screen.blit(sprite.image, sprite.rect)

        draw_hud(screen, score, lives, font, ship)
        pygame.display.flip()

    pygame.quit()


def draw_starfield(screen, stars, dt):
    for s in stars:
        s[1] += (20 + s[2]) * (dt if dt > 0 else 1/60)
        if s[1] > HEIGHT:
            s[0] = random.randrange(0, WIDTH)
            s[1] = -2
        size = 1 if s[2] < 40 else 2
        screen.fill(WHITE if size == 1 else (200, 200, 255), (int(s[0]), int(s[1]), size, size))


def draw_boost_trail(screen, ship):
    x, y = ship.rect.center
    points = [(x-8, y+20), (x+8, y+20), (x, y+40)]
    pygame.draw.polygon(screen, (255, 140, 30), points)
    pygame.draw.polygon(screen, (255, 220, 80), [(x-4, y+22), (x+4, y+22), (x, y+34)])


def draw_hud(screen, score, lives, font, ship):
    score_surf = font.render(f"Score: {score}", True, WHITE)
    lives_surf = font.render("Lives: " + "❤"*lives, True, RED)
    ammo_text = "Reloading..." if ship.reloading else f"Ammo: {ship.ammo}/{MAX_AMMO}"
    ammo_surf = font.render(ammo_text, True, YELLOW)
    screen.blit(score_surf, (8, 8))
    screen.blit(lives_surf, (8, 34))
    screen.blit(ammo_surf, (8, 60))


def game_over(screen, score, font, bigfont, highscores):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    text = bigfont.render("GAME OVER", True, WHITE)
    screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2 - 40)))
    sub = font.render(f"Your score: {score}   Press any key to continue", True, WHITE)
    screen.blit(sub, sub.get_rect(center=(WIDTH//2, HEIGHT//2 + 20)))
    y = HEIGHT//2 + 70
    hs_s = font.render("Recent scores: " + (", ".join(str(x) for x in highscores) if highscores else "none"), True, WHITE)
    screen.blit(hs_s, hs_s.get_rect(center=(WIDTH//2, y)))
    pygame.display.flip()
    waiting = True
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if e.type == pygame.KEYDOWN:
                waiting = False


if __name__ == "__main__":
    main()
