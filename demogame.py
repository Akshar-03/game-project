import pygame
import sys
import random

# initialize pygame
pygame.init()

# screen setup
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Runner Game")

# colors
WHITE = (255, 255, 255)
BLUE = (50, 100, 200)
RED = (200, 50, 50)

# player setup
player_size = 40
player_x = 100  # stays fixed (screen moves instead)
player_y = HEIGHT - player_size
velocity_y = 0
gravity = 1.5
jump_strength = -20
can_double_jump = True  # allow one extra jump in air

# obstacle setup
obstacles = []
obstacle_width = 40
obstacle_speed = 10
spawn_delay = 1500  # milliseconds
last_spawn_time = pygame.time.get_ticks()

# clock & font
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# score
score = 0

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # close window
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if player_y == HEIGHT - player_size:  # jump from ground
                    velocity_y = jump_strength
                    can_double_jump = True
                elif can_double_jump:  # double jump
                    velocity_y = jump_strength
                    can_double_jump = False

        if event.type == pygame.MOUSEBUTTONDOWN:  # mouse click
            if player_y == HEIGHT - player_size:  # jump from ground
                velocity_y = jump_strength
                can_double_jump = True
            elif can_double_jump:  # double jump
                velocity_y = jump_strength
                can_double_jump = False

    # gravity effect
    velocity_y += gravity
    player_y += velocity_y

    # stop at ground
    if player_y > HEIGHT - player_size:
        player_y = HEIGHT - player_size
        velocity_y = 0
        can_double_jump = True  # reset double jump when touching ground

    # spawn obstacles
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time > spawn_delay:
        obstacle_x = WIDTH
        obstacle_height = random.randint(40, 120)  # random height
        obstacle_y = HEIGHT - obstacle_height
        obstacles.append(pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height))
        last_spawn_time = current_time

    # move obstacles
    for obstacle in obstacles:
        obstacle.x -= obstacle_speed

    # remove obstacles off screen
    obstacles = [ob for ob in obstacles if ob.x + obstacle_width > 0]

    # check collisions
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            print("Game Over! Final Score:", score)
            pygame.quit()
            sys.exit()

    # update score
    score += 1

    # draw
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, player_rect)  # player
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)  # obstacles

    # draw score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)  # 30 FPS
