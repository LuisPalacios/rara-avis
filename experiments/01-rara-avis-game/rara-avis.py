import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rara Avis - Flappy Bird Clone")

# Colors
SKY_BLUE = (135, 206, 235)
GROUND_COLOR = (101, 67, 33)
PIPE_GREEN = (94, 185, 94)
BIRD_YELLOW = (255, 255, 0)
BIRD_ORANGE = (255, 165, 0)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 149, 237)
RED = (220, 20, 60)
GREEN = (50, 205, 50)

# Game variables
FPS = 60
GRAVITY = 0.5
FLAP_STRENGTH = -8
PIPE_SPEED = 3
PIPE_GAP = 180
PIPE_FREQUENCY = 1800  # milliseconds
GROUND_HEIGHT = 100
BIRD_WIDTH, BIRD_HEIGHT = 40, 30
PIPE_WIDTH = 70

# Font setup
font_large = pygame.font.SysFont("Arial", 48, bold=True)
font_medium = pygame.font.SysFont("Arial", 36)
font_small = pygame.font.SysFont("Arial", 24)

class Bird:
    def __init__(self):
        self.x = WIDTH // 3
        self.y = HEIGHT // 2
        self.velocity = 0
        self.alive = True
        self.flap_count = 0
        self.wing_angle = 0
        self.wing_direction = 1

    def flap(self):
        if self.alive:
            self.velocity = FLAP_STRENGTH
            self.flap_count += 1

    def update(self):
        # Apply gravity
        self.velocity += GRAVITY
        self.y += self.velocity

        # Update wing animation
        self.wing_angle += 0.2 * self.wing_direction
        if abs(self.wing_angle) > 0.5:
            self.wing_direction *= -1

        # Check if bird hits the ground or ceiling
        if self.y >= HEIGHT - GROUND_HEIGHT - BIRD_HEIGHT:
            self.y = HEIGHT - GROUND_HEIGHT - BIRD_HEIGHT
            self.alive = False
        if self.y <= 0:
            self.y = 0
            self.velocity = 0

    def draw(self):
        # Draw bird body
        pygame.draw.ellipse(screen, BIRD_YELLOW, (self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT))

        # Draw bird eye
        pygame.draw.circle(screen, (0, 0, 0), (self.x + BIRD_WIDTH - 10, self.y + 10), 5)
        pygame.draw.circle(screen, (255, 255, 255), (self.x + BIRD_WIDTH - 12, self.y + 8), 2)

        # Draw bird beak
        beak_points = [
            (self.x + BIRD_WIDTH, self.y + 15),
            (self.x + BIRD_WIDTH + 10, self.y + 12),
            (self.x + BIRD_WIDTH + 10, self.y + 18)
        ]
        pygame.draw.polygon(screen, BIRD_ORANGE, beak_points)

        # Draw wing
        wing_points = [
            (self.x + 10, self.y + 15),
            (self.x + 20, self.y + 15 + self.wing_angle * 10),
            (self.x + 30, self.y + 15)
        ]
        pygame.draw.polygon(screen, (255, 200, 0), wing_points)

    def get_mask(self):
        # Simple collision mask for bird
        return pygame.Rect(self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT)

class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(100, HEIGHT - GROUND_HEIGHT - PIPE_GAP - 100)
        self.top_pipe = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom_pipe = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP)
        self.passed = False
        self.scored = False

    def update(self):
        self.x -= PIPE_SPEED
        self.top_pipe.x = self.x
        self.bottom_pipe.x = self.x

    def draw(self):
        # Draw top pipe
        pygame.draw.rect(screen, PIPE_GREEN, self.top_pipe)
        pygame.draw.rect(screen, (50, 120, 50), self.top_pipe, 3)

        # Draw pipe cap
        cap_rect = pygame.Rect(self.x - 5, self.height - 20, PIPE_WIDTH + 10, 20)
        pygame.draw.rect(screen, PIPE_GREEN, cap_rect)
        pygame.draw.rect(screen, (50, 120, 50), cap_rect, 3)

        # Draw bottom pipe
        pygame.draw.rect(screen, PIPE_GREEN, self.bottom_pipe)
        pygame.draw.rect(screen, (50, 120, 50), self.bottom_pipe, 3)

        # Draw pipe cap
        cap_rect = pygame.Rect(self.x - 5, self.height + PIPE_GAP, PIPE_WIDTH + 10, 20)
        pygame.draw.rect(screen, PIPE_GREEN, cap_rect)
        pygame.draw.rect(screen, (50, 120, 50), cap_rect, 3)

    def collide(self, bird):
        bird_mask = bird.get_mask()
        return bird_mask.colliderect(self.top_pipe) or bird_mask.colliderect(self.bottom_pipe)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hovered = False

    def draw(self):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (30, 30, 30), self.rect, 3, border_radius=10)

        text_surf = font_medium.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

    def check_click(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, -0.5)
        self.vy = random.uniform(-1, 1)
        self.lifetime = random.randint(20, 40)
        self.size = random.randint(3, 6)
        self.color = random.choice([
            (255, 255, 100),  # Light yellow
            (255, 220, 50),   # Golden
            (255, 200, 0),    # Yellow
            (255, 180, 50),   # Orange-yellow
        ])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.size = max(1, self.size - 0.1)

    def draw(self):
        if self.lifetime > 0:
            alpha = int(255 * (self.lifetime / 40))
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

    def is_alive(self):
        return self.lifetime > 0

class Cloud:
    def __init__(self):
        self.x = WIDTH + random.randint(0, 300)
        self.y = random.randint(50, 200)
        self.speed = random.uniform(0.5, 1.5)
        self.size = random.randint(30, 60)

    def update(self):
        self.x -= self.speed
        if self.x < -100:
            self.x = WIDTH + 50
            self.y = random.randint(50, 200)

    def draw(self):
        pygame.draw.circle(screen, (250, 250, 250), (self.x, self.y), self.size)
        pygame.draw.circle(screen, (250, 250, 250), (self.x + self.size*0.8, self.y - self.size*0.2), self.size*0.7)
        pygame.draw.circle(screen, (250, 250, 250), (self.x + self.size*1.5, self.y), self.size*0.9)

def draw_ground():
    pygame.draw.rect(screen, GROUND_COLOR, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

    # Draw grass
    pygame.draw.rect(screen, (34, 139, 34), (0, HEIGHT - GROUND_HEIGHT, WIDTH, 20))

    # Draw ground details
    for i in range(0, WIDTH, 30):
        pygame.draw.line(screen, (80, 50, 20), (i, HEIGHT - GROUND_HEIGHT + 10),
                         (i + 15, HEIGHT - GROUND_HEIGHT + 10), 2)

def draw_background():
    # Sky
    screen.fill(SKY_BLUE)

    # Draw sun
    pygame.draw.circle(screen, (255, 255, 200), (700, 80), 60)
    pygame.draw.circle(screen, (255, 255, 100), (700, 80), 40)

    # Draw clouds
    for cloud in clouds:
        cloud.draw()

def draw_score(score, high_score):
    score_text = font_medium.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (20, 20))

    high_score_text = font_medium.render(f"High Score: {high_score}", True, TEXT_COLOR)
    screen.blit(high_score_text, (20, 70))

def draw_game_over(score, high_score, restart_button):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    game_over_text = font_large.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//3))

    score_text = font_medium.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))

    high_score_text = font_medium.render(f"High Score: {high_score}", True, TEXT_COLOR)
    screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//2 + 50))

    # Draw restart button
    restart_button.draw()

def draw_start_screen():
    title_text = font_large.render("RARA AVIS", True, (255, 215, 0))
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//4))

    instructions = [
        "Press SPACE or CLICK to flap",
        "Avoid pipes and don't hit the ground",
        "Press P to pause",
        "Press SPACE or ENTER to start"
    ]

    for i, line in enumerate(instructions):
        text = font_small.render(line, True, TEXT_COLOR)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 + i*40))

    # Draw a simple bird in the start screen
    pygame.draw.ellipse(screen, BIRD_YELLOW, (WIDTH//2 - 50, HEIGHT//3, 40, 30))
    pygame.draw.circle(screen, (0, 0, 0), (WIDTH//2 - 10, HEIGHT//3 + 10), 5)
    pygame.draw.polygon(screen, BIRD_ORANGE, [
        (WIDTH//2 + 30, HEIGHT//3 + 15),
        (WIDTH//2 + 40, HEIGHT//3 + 12),
        (WIDTH//2 + 40, HEIGHT//3 + 18)
    ])

def draw_paused():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))

    paused_text = font_large.render("PAUSED", True, TEXT_COLOR)
    screen.blit(paused_text, (WIDTH//2 - paused_text.get_width()//2, HEIGHT//2 - 50))

    resume_text = font_small.render("Press P to resume", True, TEXT_COLOR)
    screen.blit(resume_text, (WIDTH//2 - resume_text.get_width()//2, HEIGHT//2 + 20))

def main():
    global clouds

    clock = pygame.time.Clock()
    bird = Bird()
    pipes = []
    particles = []
    score = 0
    high_score = 0
    last_pipe = pygame.time.get_ticks()
    game_state = "start"  # start, playing, paused, game_over
    clouds = [Cloud() for _ in range(5)]
    paused = False

    # Create buttons
    restart_button = Button(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50, "RESTART")

    # Main game loop
    while True:
        current_time = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_state == "start":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        game_state = "playing"

            elif game_state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.flap()
                    if event.key == pygame.K_p:
                        paused = True
                        game_state = "paused"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    bird.flap()

            elif game_state == "paused":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
                        game_state = "playing"

            elif game_state == "game_over":
                restart_button.check_hover(mouse_pos)
                restart_pressed = restart_button.check_click(mouse_pos, event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    restart_pressed = True
                if restart_pressed:
                    # Reset game
                    bird = Bird()
                    pipes = []
                    particles = []
                    score = 0
                    last_pipe = current_time
                    game_state = "playing"

        # Update game objects
        if game_state == "playing":
            bird.update()

            # Spawn particles behind the bird
            if random.random() < 0.5:  # 50% chance each frame
                particles.append(Particle(bird.x, bird.y + BIRD_HEIGHT // 2))

            # Update particles
            for particle in particles[:]:
                particle.update()
                if not particle.is_alive():
                    particles.remove(particle)

            # Generate new pipes
            if current_time - last_pipe > PIPE_FREQUENCY:
                pipes.append(Pipe())
                last_pipe = current_time

            # Update pipes
            for pipe in pipes[:]:
                pipe.update()

                # Check if bird passed the pipe
                if not pipe.passed and pipe.x + PIPE_WIDTH < bird.x:
                    pipe.passed = True
                    score += 1

                # Check for collisions
                if pipe.collide(bird):
                    bird.alive = False

                # Remove pipes that are off screen
                if pipe.x + PIPE_WIDTH < 0:
                    pipes.remove(pipe)

            # Check if bird is dead
            if not bird.alive:
                game_state = "game_over"
                if score > high_score:
                    high_score = score

        # Update clouds
        for cloud in clouds:
            cloud.update()

        # Drawing
        draw_background()

        # Draw particles (behind bird)
        for particle in particles:
            particle.draw()

        # Draw pipes
        for pipe in pipes:
            pipe.draw()

        # Draw ground
        draw_ground()

        # Draw bird
        bird.draw()

        # Draw score
        if game_state == "playing" or game_state == "game_over" or game_state == "paused":
            draw_score(score, high_score)

        # Draw screens
        if game_state == "start":
            draw_start_screen()
        elif game_state == "paused":
            draw_paused()
        elif game_state == "game_over":
            draw_game_over(score, high_score, restart_button)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
