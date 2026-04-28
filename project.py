import random
import sys
import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Sky")
clock = pygame.time.Clock()

font_large = pygame.font.SysFont(None, 64)
font_medium = pygame.font.SysFont(None, 36)
font_small = pygame.font.SysFont(None, 28)

BLACK = (15, 15, 20)
BLUE = (70, 130, 220)
RED = (220, 70, 70)
WHITE = (255, 255, 255)
DARK_GRAY = (40, 40, 50)

PLAYER_WIDTH = 60
PLAYER_HEIGHT = 20
PLAYER_SPEED = 7

HAZARD_WIDTH = 35
HAZARD_HEIGHT = 35
HAZARD_BASE_SPEED = 4
HAZARD_SPAWN_DELAY = 700


class Player:
    def __init__(self):
        self.rect = pygame.Rect(
            WIDTH // 2 - PLAYER_WIDTH // 2,
            HEIGHT - 60,
            PLAYER_WIDTH,
            PLAYER_HEIGHT
        )
        self.speed = PLAYER_SPEED

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect, border_radius=6)


class Hazard:
    def __init__(self, speed_bonus):
        self.rect = pygame.Rect(
            random.randint(0, WIDTH - HAZARD_WIDTH),
            -HAZARD_HEIGHT,
            HAZARD_WIDTH,
            HAZARD_HEIGHT
        )
        self.speed = HAZARD_BASE_SPEED + random.uniform(0, 2) + speed_bonus

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect, border_radius=4)


def draw_background(surface):
    surface.fill(BLACK)
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(surface, DARK_GRAY, (0, y), (WIDTH, y), 1)


def draw_text(surface, text, font, color, x, y):
    image = font.render(text, True, color)
    rect = image.get_rect(center=(x, y))
    surface.blit(image, rect)


def draw_ui(surface, score):
    score_text = font_medium.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (20, 20))


def draw_game_over(surface, score):
    draw_text(surface, "Game Over", font_large, WHITE, WIDTH // 2, HEIGHT // 2 - 40)
    draw_text(surface, f"Final Score: {score}", font_medium, WHITE, WIDTH // 2, HEIGHT // 2 + 10)
    draw_text(surface, "Close the window to quit", font_small, WHITE, WIDTH // 2, HEIGHT // 2 + 50)


def main():
    player = Player()
    hazards = []

    last_spawn_time = pygame.time.get_ticks()
    start_time = pygame.time.get_ticks()

    running = True
    game_over = False
    final_score = 0

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = pygame.time.get_ticks()
        elapsed_seconds = (current_time - start_time) // 1000
        speed_bonus = elapsed_seconds * 0.15
        current_spawn_delay = max(250, HAZARD_SPAWN_DELAY - elapsed_seconds * 15)

        if not game_over:
            keys = pygame.key.get_pressed()
            player.update(keys)

            if current_time - last_spawn_time >= current_spawn_delay:
                hazards.append(Hazard(speed_bonus))
                last_spawn_time = current_time

            for hazard in hazards:
                hazard.update()

            hazards = [hazard for hazard in hazards if hazard.rect.top <= HEIGHT]

            for hazard in hazards:
                if player.rect.colliderect(hazard.rect):
                    game_over = True
                    final_score = elapsed_seconds
                    break

        draw_background(screen)

        if not game_over:
            player.draw(screen)

            for hazard in hazards:
                hazard.draw(screen)

            draw_ui(screen, elapsed_seconds)
        else:
            draw_game_over(screen, final_score)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()