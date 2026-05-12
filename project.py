import random
import sys
import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frozen Summit")
clock = pygame.time.Clock()

background_image = pygame.image.load("assets/snow_mountain.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

font_large = pygame.font.SysFont(None, 64)
font_medium = pygame.font.SysFont(None, 36)
font_small = pygame.font.SysFont(None, 28)

BLACK = (15, 15, 20)
BLUE = (70, 130, 220)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
DARK_TEXT = (25, 25, 35)
YELLOW = (180, 130, 20)
GREEN = (20, 120, 60)
SKIN = (240, 210, 180)
ICE_BLUE = (180, 220, 255)
TEXT_BOX = (245, 245, 245)

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 55
PLAYER_SPEED = 7

HAZARD_BASE_SPEED = 4
HAZARD_SPAWN_DELAY = 700

SLOWMO_DURATION = 2000
SLOWMO_COOLDOWN = 5000


class Player:
    def __init__(self):
        self.rect = pygame.Rect(
            WIDTH // 2 - PLAYER_WIDTH // 2,
            HEIGHT - 90,
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
        head_center = (self.rect.centerx, self.rect.top + 10)
        body_rect = pygame.Rect(self.rect.centerx - 11, self.rect.top + 22, 22, 25)

        pygame.draw.circle(surface, SKIN, head_center, 10)
        pygame.draw.circle(surface, BLACK, head_center, 10, 2)

        pygame.draw.rect(surface, BLUE, body_rect, border_radius=5)
        pygame.draw.rect(surface, BLACK, body_rect, 2, border_radius=5)

        scarf_rect = pygame.Rect(self.rect.centerx - 13, self.rect.top + 19, 26, 7)
        pygame.draw.rect(surface, ICE_BLUE, scarf_rect, border_radius=4)
        pygame.draw.rect(surface, BLACK, scarf_rect, 1, border_radius=4)


class Hazard:
    def __init__(self, speed_bonus):
        self.width = random.randint(20, 40)
        self.height = random.randint(45, 95)
        self.rect = pygame.Rect(
            random.randint(0, WIDTH - self.width),
            -self.height,
            self.width,
            self.height
        )
        self.speed = HAZARD_BASE_SPEED + random.uniform(0, 2) + speed_bonus

    def update(self, time_scale):
        self.rect.y += self.speed * time_scale

    def draw(self, surface):
        top_left = (self.rect.left, self.rect.top)
        top_right = (self.rect.right, self.rect.top)
        bottom = (self.rect.centerx, self.rect.bottom)

        pygame.draw.polygon(surface, WHITE, [top_left, top_right, bottom])
        pygame.draw.polygon(surface, BLACK, [top_left, top_right, bottom], 3)
        pygame.draw.polygon(surface, ICE_BLUE, [top_left, top_right, bottom], 1)


class SnowParticle:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(1, 3)
        self.size = random.randint(1, 3)

    def update(self):
        self.y += self.speed

        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.size)


class BurstParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_speed = random.uniform(-4, 4)
        self.y_speed = random.uniform(-4, 4)
        self.life = 45
        self.size = random.randint(3, 6)

    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, ICE_BLUE, (int(self.x), int(self.y)), self.size)


def create_snow_particles():
    particles = []

    for i in range(70):
        particles.append(SnowParticle())

    return particles


def create_burst_particles(x, y):
    particles = []

    for i in range(35):
        particles.append(BurstParticle(x, y))

    return particles


def draw_background(surface, snow_particles):
    surface.blit(background_image, (0, 0))

    for particle in snow_particles:
        particle.update()
        particle.draw(surface)


def draw_text(surface, text, font, color, x, y):
    image = font.render(text, True, color)
    rect = image.get_rect(center=(x, y))

    box_rect = rect.inflate(20, 12)
    pygame.draw.rect(surface, TEXT_BOX, box_rect, border_radius=8)
    pygame.draw.rect(surface, BLACK, box_rect, 2, border_radius=8)

    surface.blit(image, rect)


def draw_ui(surface, score, slowmo_active, slowmo_ready, cooldown_left):
    score_text = font_medium.render(f"Score: {score}", True, DARK_TEXT)
    score_rect = score_text.get_rect(topleft=(20, 20))

    score_box = score_rect.inflate(18, 10)
    pygame.draw.rect(surface, TEXT_BOX, score_box, border_radius=6)
    pygame.draw.rect(surface, BLACK, score_box, 2, border_radius=6)
    surface.blit(score_text, score_rect)

    if slowmo_active:
        status_text = "Slow Motion: ACTIVE"
        status_color = YELLOW
    elif slowmo_ready:
        status_text = "Slow Motion: READY (SPACE)"
        status_color = GREEN
    else:
        status_text = f"Slow Motion Cooldown: {cooldown_left:.1f}s"
        status_color = GRAY

    slowmo_text = font_small.render(status_text, True, status_color)
    slowmo_rect = slowmo_text.get_rect(topleft=(20, 60))

    slowmo_box = slowmo_rect.inflate(18, 10)
    pygame.draw.rect(surface, TEXT_BOX, slowmo_box, border_radius=6)
    pygame.draw.rect(surface, BLACK, slowmo_box, 2, border_radius=6)
    surface.blit(slowmo_text, slowmo_rect)


def start_screen(snow_particles):
    while True:
        clock.tick(FPS)
        draw_background(screen, snow_particles)

        draw_text(screen, "Frozen Summit", font_large, DARK_TEXT, WIDTH // 2, HEIGHT // 2 - 90)
        draw_text(screen, "Avoid the falling icicles for as long as possible.", font_small, DARK_TEXT, WIDTH // 2, HEIGHT // 2 - 25)
        draw_text(screen, "Move with A/D or Left/Right", font_small, DARK_TEXT, WIDTH // 2, HEIGHT // 2 + 10)
        draw_text(screen, "Press SPACE to slow time", font_small, DARK_TEXT, WIDTH // 2, HEIGHT // 2 + 45)
        draw_text(screen, "Press ENTER to Start", font_medium, DARK_TEXT, WIDTH // 2, HEIGHT // 2 + 110)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return


def game_over_screen(score, snow_particles, burst_particles):
    while True:
        clock.tick(FPS)
        draw_background(screen, snow_particles)

        for particle in burst_particles:
            particle.update()
            particle.draw(screen)

        burst_particles = [particle for particle in burst_particles if particle.life > 0]

        draw_text(screen, "Game Over", font_large, DARK_TEXT, WIDTH // 2, HEIGHT // 2 - 70)
        draw_text(screen, f"Final Score: {score}", font_medium, DARK_TEXT, WIDTH // 2, HEIGHT // 2)
        draw_text(screen, "Press R to Restart", font_medium, DARK_TEXT, WIDTH // 2, HEIGHT // 2 + 65)
        draw_text(screen, "Press ESC to Quit", font_small, DARK_TEXT, WIDTH // 2, HEIGHT // 2 + 110)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def run_game(snow_particles):
    player = Player()
    hazards = []

    last_spawn_time = pygame.time.get_ticks()
    start_time = pygame.time.get_ticks()

    slowmo_active = False
    slowmo_start_time = 0
    last_slowmo_used = -SLOWMO_COOLDOWN

    while True:
        clock.tick(FPS)

        current_time = pygame.time.get_ticks()
        elapsed_seconds = (current_time - start_time) // 1000
        speed_bonus = elapsed_seconds * 0.15
        current_spawn_delay = max(250, HAZARD_SPAWN_DELAY - elapsed_seconds * 15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if current_time - last_slowmo_used >= SLOWMO_COOLDOWN:
                        slowmo_active = True
                        slowmo_start_time = current_time
                        last_slowmo_used = current_time

        if slowmo_active and current_time - slowmo_start_time >= SLOWMO_DURATION:
            slowmo_active = False

        time_scale = 0.45 if slowmo_active else 1.0

        keys = pygame.key.get_pressed()
        player.update(keys)

        if current_time - last_spawn_time >= current_spawn_delay:
            hazards.append(Hazard(speed_bonus))
            last_spawn_time = current_time

        for hazard in hazards:
            hazard.update(time_scale)

        hazards = [hazard for hazard in hazards if hazard.rect.top <= HEIGHT]

        for hazard in hazards:
            if player.rect.colliderect(hazard.rect):
                burst_particles = create_burst_particles(player.rect.centerx, player.rect.centery)
                return elapsed_seconds, burst_particles

        draw_background(screen, snow_particles)
        player.draw(screen)

        for hazard in hazards:
            hazard.draw(screen)

        slowmo_ready = current_time - last_slowmo_used >= SLOWMO_COOLDOWN
        cooldown_left = max(0, (SLOWMO_COOLDOWN - (current_time - last_slowmo_used)) / 1000)

        draw_ui(screen, elapsed_seconds, slowmo_active, slowmo_ready, cooldown_left)

        pygame.display.flip()


def main():
    snow_particles = create_snow_particles()
    start_screen(snow_particles)

    while True:
        score, burst_particles = run_game(snow_particles)
        game_over_screen(score, snow_particles, burst_particles)


if __name__ == "__main__":
    main()