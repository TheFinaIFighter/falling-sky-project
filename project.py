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
HAZARD_SPEED = 5
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
    def __init__(self):
        self.rect = pygame.Rect(
            random.randint(0, WIDTH - HAZARD_WIDTH),
            -HAZARD_HEIGHT,
            HAZARD_WIDTH,
            HAZARD_HEIGHT
        )
        self.speed = HAZARD_SPEED

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


def draw_game_over(surface):
    draw_text(surface, "Game Over", font_large, WHITE, WIDTH // 2, HEIGHT // 2 - 20)
    draw_text(surface, "Close the window to quit", font_medium, WHITE, WIDTH // 2, HEIGHT // 2 + 35)


def main():
    player = Player()
    hazards = []

    last_spawn_time = pygame.time.get_ticks()
    running = True
    game_over = False

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            keys = pygame.key.get_pressed()
            player.update(keys)

            current_time = pygame.time.get_ticks()
            if current_time - last_spawn_time >= HAZARD_SPAWN_DELAY:
                hazards.append(Hazard())
                last_spawn_time = current_time

            for hazard in hazards:
                hazard.update()

            hazards = [hazard for hazard in hazards if hazard.rect.top <= HEIGHT]

            for hazard in hazards:
                if player.rect.colliderect(hazard.rect):
                    game_over = True
                    break

        draw_background(screen)

        if not game_over:
            player.draw(screen)
            for hazard in hazards:
                hazard.draw(screen)
        else:
            draw_game_over(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()