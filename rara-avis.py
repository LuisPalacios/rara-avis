import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GROUND_HEIGHT = 100
GRAVITY = 0.5
JUMP_STRENGTH = -8
PIPE_SPEED = 3
PIPE_GAP = 200
PIPE_FREQUENCY = 1800  # milliseconds
PIPE_WIDTH = 80

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
SKY_BLUE = (135, 206, 235)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.radius = 20
        self.alive = True
        self.rotation = 0

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def update(self):
        # Apply gravity
        self.velocity += GRAVITY
        self.y += self.velocity

        # Rotate based on velocity
        self.rotation = max(-30, min(self.velocity * 3, 90))

        # Keep player on screen
        if self.y < self.radius:
            self.y = self.radius
            self.velocity = 0

        if self.y > HEIGHT - GROUND_HEIGHT - self.radius:
            self.y = HEIGHT - GROUND_HEIGHT - self.radius
            self.velocity = 0
            self.alive = False

    def draw(self, screen):
        # Draw player as a circle with rotation effect
        surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, YELLOW, (self.radius, self.radius), self.radius)
        pygame.draw.circle(surface, BLACK, (self.radius - 5, self.radius - 5), 5)
        pygame.draw.circle(surface, BLACK, (self.radius + 5, self.radius - 5), 5)
        rotated = pygame.transform.rotate(surface, self.rotation)
        rect = rotated.get_rect(center=(self.x, self.y))
        screen.blit(rotated, rect)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                          self.radius * 2, self.radius * 2)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = PIPE_WIDTH
        self.gap_y = random.randint(150, HEIGHT - GROUND_HEIGHT - 150)
        self.passed = False
        self.top_height = self.gap_y - PIPE_GAP // 2
        self.bottom_y = self.gap_y + PIPE_GAP // 2

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self, screen):
        # Draw top pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(screen, (0, 100, 0), (self.x, self.top_height - 20, self.width, 20))

        # Draw bottom pipe
        pygame.draw.rect(screen, GREEN, (self.x, self.bottom_y, self.width, HEIGHT - self.bottom_y))
        pygame.draw.rect(screen, (0, 100, 0), (self.x, self.bottom_y, self.width, 20))

    def collide(self, player):
        player_rect = player.get_rect()

        # Top pipe collision
        top_pipe_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        # Bottom pipe collision
        bottom_pipe_rect = pygame.Rect(self.x, self.bottom_y, self.width, HEIGHT - self.bottom_y)

        return player_rect.colliderect(top_pipe_rect) or player_rect.colliderect(bottom_pipe_rect)

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity_x = random.uniform(-3, 3)
        self.velocity_y = random.uniform(-3, 3)
        self.life = 30
        self.max_life = 30
        self.size = random.randint(2, 5)

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.life -= 1

    def is_dead(self):
        return self.life <= 0

    def draw(self, screen):
        alpha = int(255 * (self.life / self.max_life))
        color = (255, 255, 0, alpha)
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), self.size)

class Cloud:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.uniform(0.5, 1.5)

    def update(self):
        self.x -= self.speed
        if self.x < -100:
            self.x = WIDTH + 100
            self.y = random.randint(50, 200)

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 20)
        pygame.draw.circle(screen, WHITE, (int(self.x + 15), int(self.y - 10)), 15)
        pygame.draw.circle(screen, WHITE, (int(self.x + 30), int(self.y)), 20)
        pygame.draw.circle(screen, WHITE, (int(self.x + 15), int(self.y + 10)), 15)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Rara Avis")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_large = pygame.font.SysFont(None, 72)
        self.font_medium = pygame.font.SysFont(None, 36)
        self.font_small = pygame.font.SysFont(None, 24)

        # Game state
        self.state = "menu"  # menu, playing, paused, game_over

        # Game objects
        self.player = Player(100, HEIGHT // 2)
        self.pipes = []
        self.particles = []
        self.clouds = []
        self.score = 0
        self.high_score = 0
        self.last_pipe_time = 0

        # Create clouds
        for _ in range(5):
            self.clouds.append(Cloud(random.randint(0, WIDTH), random.randint(50, 200)))

    def reset_game(self):
        self.player = Player(100, HEIGHT // 2)
        self.pipes = []
        self.particles = []
        self.score = 0
        self.last_pipe_time = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if self.state == "menu" and event.key == pygame.K_SPACE:
                    self.state = "playing"
                elif self.state == "playing" and event.key == pygame.K_SPACE:
                    self.player.jump()
                elif self.state == "game_over" and event.key == pygame.K_SPACE:
                    self.reset_game()
                    self.state = "playing"
                elif event.key == pygame.K_p:
                    if self.state == "playing":
                        self.state = "paused"
                    elif self.state == "paused":
                        self.state = "playing"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == "menu":
                    self.state = "playing"
                elif self.state == "playing":
                    self.player.jump()
                elif self.state == "game_over":
                    self.reset_game()
                    self.state = "playing"

        return True

    def update(self):
        current_time = pygame.time.get_ticks()

        # Update player if playing
        if self.state == "playing":
            self.player.update()

            # Check collision with ground
            if not self.player.alive:
                self.state = "game_over"
                if self.score > self.high_score:
                    self.high_score = self.score

            # Generate pipes
            if current_time - self.last_pipe_time > PIPE_FREQUENCY:
                self.pipes.append(Pipe(WIDTH))
                self.last_pipe_time = current_time

            # Update pipes and check collisions
            for pipe in self.pipes[:]:
                pipe.update()

                # Remove off-screen pipes
                if pipe.x + pipe.width < 0:
                    self.pipes.remove(pipe)
                    continue

                # Check collision
                if pipe.collide(self.player):
                    self.state = "game_over"
                    if self.score > self.high_score:
                        self.high_score = self.score

                # Check if passed pipe
                if not pipe.passed and pipe.x + pipe.width < self.player.x:
                    pipe.passed = True
                    self.score += 1

            # Create particles for player movement
            if current_time % 5 == 0:
                self.particles.append(Particle(self.player.x - 10, self.player.y))

            # Update particles
            for particle in self.particles[:]:
                particle.update()
                if particle.is_dead():
                    self.particles.remove(particle)

            # Update clouds
            for cloud in self.clouds:
                cloud.update()

        # Update particles even when not playing
        for particle in self.particles[:]:
            particle.update()
            if particle.is_dead():
                self.particles.remove(particle)

    def draw_background(self):
        # Sky gradient
        for y in range(0, HEIGHT, 2):
            color_value = max(0, min(255, int(100 + (y / HEIGHT) * 155)))
            pygame.draw.line(self.screen, (color_value, min(color_value + 50, 255), 255),
                        (0, y), (WIDTH, y), 2)

        # Draw sun
        pygame.draw.circle(self.screen, YELLOW, (700, 80), 50)

        # Draw sun rays
        for i in range(12):
            angle = i * 30
            start_x = 700 + 50 * math.cos(math.radians(angle))
            start_y = 80 + 50 * math.sin(math.radians(angle))
            end_x = 700 + 70 * math.cos(math.radians(angle))
            end_y = 80 + 70 * math.sin(math.radians(angle))
            pygame.draw.line(self.screen, YELLOW, (start_x, start_y), (end_x, end_y), 3)

    def draw(self):
        # Clear screen with background
        self.draw_background()

        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(self.screen)

        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)

        # Draw ground
        pygame.draw.rect(self.screen, BROWN, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

        # Draw grass
        pygame.draw.rect(self.screen, (0, 150, 0), (0, HEIGHT - GROUND_HEIGHT, WIDTH, 20))

        # Draw ground details
        for i in range(0, WIDTH, 30):
            pygame.draw.line(self.screen, (100, 70, 0), (i, HEIGHT - GROUND_HEIGHT + 20),
                           (i + 15, HEIGHT - GROUND_HEIGHT + 20), 3)

        # Draw player
        if self.state == "playing" or self.state == "game_over":
            self.player.draw(self.screen)

        # Draw UI based on state
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "playing":
            self.draw_game_ui()
        elif self.state == "paused":
            self.draw_pause_screen()
        elif self.state == "game_over":
            self.draw_game_over()

    def draw_menu(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Title
        title_text = self.font_large.render("FLIPPYBLOCK EXTREME", True, YELLOW)
        self.screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 100))

        # Instructions
        instructions = [
            "Press SPACE or CLICK to flap",
            "Avoid pipes and don't hit the ground",
            "Press SPACE to start"
        ]

        for i, line in enumerate(instructions):
            text = self.font_small.render(line, True, WHITE)
            self.screen.blit(text, (WIDTH//2 - text.get_width()//2, 250 + i * 50))

        # High score
        high_score_text = self.font_medium.render(f"High Score: {self.high_score}", True, YELLOW)
        self.screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, 450))

    def draw_game_ui(self):
        # Draw score
        score_text = self.font_medium.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))

        # Draw high score
        high_score_text = self.font_medium.render(f"High Score: {self.high_score}", True, WHITE)
        self.screen.blit(high_score_text, (20, 70))

    def draw_pause_screen(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # Pause text
        pause_text = self.font_large.render("PAUSED", True, YELLOW)
        self.screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2 - 50))

        # Continue instructions
        continue_text = self.font_small.render("Press P to continue", True, WHITE)
        self.screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 50))

    def draw_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # Game over text
        game_over_text = self.font_large.render("GAME OVER", True, RED)
        self.screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 100))

        # Score
        score_text = self.font_medium.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))

        # High score
        high_score_text = self.font_medium.render(f"High Score: {self.high_score}", True, WHITE)
        self.screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//2 + 50))

        # Restart instructions
        restart_text = self.font_small.render("Press SPACE or CLICK to restart", True, WHITE)
        self.screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 120))

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

# Create and run the game
if __name__ == "__main__":
    game = Game()
    game.run()
