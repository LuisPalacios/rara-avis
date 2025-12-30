import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CAR_WIDTH = 50
CAR_HEIGHT = 80
OBSTACLE_WIDTH = 40
OBSTACLE_HEIGHT = 60
CAR_SPEED = 5
OBSTACLE_SPEED = 3
LANE_COUNT = 3
LANE_WIDTH = SCREEN_WIDTH // LANE_COUNT
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Car Game")

# Functions to generate procedural images as fallback
def create_car_image(width, height):
    """Create a car sprite procedurally"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)

    # Car body (blue)
    body_color = (30, 144, 255)  # Dodger blue
    body_rect = pygame.Rect(5, 15, width - 10, height - 20)
    pygame.draw.rect(surface, body_color, body_rect, border_radius=8)

    # Car roof/cabin (darker blue)
    cabin_color = (25, 100, 200)
    cabin_rect = pygame.Rect(10, 25, width - 20, 30)
    pygame.draw.rect(surface, cabin_color, cabin_rect, border_radius=5)

    # Windshield (light blue)
    windshield_color = (173, 216, 230)
    windshield_rect = pygame.Rect(12, 20, width - 24, 15)
    pygame.draw.rect(surface, windshield_color, windshield_rect, border_radius=3)

    # Rear window
    rear_window_rect = pygame.Rect(12, 50, width - 24, 10)
    pygame.draw.rect(surface, windshield_color, rear_window_rect, border_radius=3)

    # Wheels (dark gray)
    wheel_color = (40, 40, 40)
    pygame.draw.ellipse(surface, wheel_color, pygame.Rect(2, 5, 12, 18))
    pygame.draw.ellipse(surface, wheel_color, pygame.Rect(width - 14, 5, 12, 18))
    pygame.draw.ellipse(surface, wheel_color, pygame.Rect(2, height - 23, 12, 18))
    pygame.draw.ellipse(surface, wheel_color, pygame.Rect(width - 14, height - 23, 12, 18))

    # Headlights (yellow)
    headlight_color = (255, 255, 100)
    pygame.draw.ellipse(surface, headlight_color, pygame.Rect(12, 8, 8, 6))
    pygame.draw.ellipse(surface, headlight_color, pygame.Rect(width - 20, 8, 8, 6))

    # Taillights (red)
    taillight_color = (255, 50, 50)
    pygame.draw.ellipse(surface, taillight_color, pygame.Rect(12, height - 12, 8, 6))
    pygame.draw.ellipse(surface, taillight_color, pygame.Rect(width - 20, height - 12, 8, 6))

    return surface

def create_obstacle_image(width, height):
    """Create an obstacle sprite procedurally (traffic cone)"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)

    # Orange cone body
    cone_color = (255, 140, 0)  # Dark orange
    stripe_color = (255, 255, 255)  # White stripes

    # Draw cone shape (trapezoid)
    points = [
        (width // 2, 5),  # Top center
        (5, height - 10),  # Bottom left
        (width - 5, height - 10)  # Bottom right
    ]
    pygame.draw.polygon(surface, cone_color, points)

    # White reflective stripes
    pygame.draw.line(surface, stripe_color, (12, 20), (width - 12, 20), 4)
    pygame.draw.line(surface, stripe_color, (8, 35), (width - 8, 35), 4)

    # Base (dark gray)
    base_color = (60, 60, 60)
    pygame.draw.rect(surface, base_color, pygame.Rect(2, height - 12, width - 4, 10), border_radius=2)

    return surface

# Load images (with procedural fallback)
try:
    car_img = pygame.image.load('car.png').convert_alpha()
    car_img = pygame.transform.scale(car_img, (CAR_WIDTH, CAR_HEIGHT))
except (pygame.error, FileNotFoundError):
    print("Note: 'car.png' not found, using procedural graphics.")
    car_img = create_car_image(CAR_WIDTH, CAR_HEIGHT)

try:
    obstacle_img = pygame.image.load('obstacle.png').convert_alpha()
    obstacle_img = pygame.transform.scale(obstacle_img, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
except (pygame.error, FileNotFoundError):
    print("Note: 'obstacle.png' not found, using procedural graphics.")
    obstacle_img = create_obstacle_image(OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

# Create a font for game-over text
font = pygame.font.SysFont('Arial', 36)
small_font = pygame.font.SysFont('Arial', 24)

# Initialize mixer for sound
pygame.mixer.init()

# Try to load sound files (optional - game works without them)
collision_sound = None
background_music = None

try:
    collision_sound = pygame.mixer.Sound('collision.wav')
    collision_sound.set_volume(0.7)
except (pygame.error, FileNotFoundError):
    pass

try:
    background_music = pygame.mixer.Sound('background_music.wav')
    background_music.set_volume(0.3)
    background_music.play(-1)  # Loop indefinitely
except (pygame.error, FileNotFoundError):
    pass

if collision_sound is None and background_music is None:
    print("Note: No sound files found, running without audio.")

# Player car class
class Car:
    def __init__(self):
        # Start at bottom center
        self.x = SCREEN_WIDTH // 2 - CAR_WIDTH // 2
        self.y = SCREEN_HEIGHT - CAR_HEIGHT - 20
        self.speed = CAR_SPEED
        self.lane = 1  # Middle lane (0, 1, 2)
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT

    def update(self):
        # Keep car within screen bounds
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.x = self.lane * LANE_WIDTH + LANE_WIDTH // 2 - self.width // 2

    def move_right(self):
        if self.lane < LANE_COUNT - 1:
            self.lane += 1
            self.x = self.lane * LANE_WIDTH + LANE_WIDTH // 2 - self.width // 2

    def draw(self, screen):
        screen.blit(car_img, (self.x, self.y))

# Obstacle class
class Obstacle:
    def __init__(self):
        # Randomly select lane
        self.lane = random.randint(0, LANE_COUNT - 1)
        self.x = self.lane * LANE_WIDTH + LANE_WIDTH // 2 - OBSTACLE_WIDTH // 2
        self.y = -OBSTACLE_HEIGHT  # Start above screen
        self.speed = OBSTACLE_SPEED
        self.width = OBSTACLE_WIDTH
        self.height = OBSTACLE_HEIGHT

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        screen.blit(obstacle_img, (self.x, self.y))

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT

# Game state
class GameState:
    def __init__(self):
        self.car = Car()
        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.camera_y = 0  # Camera offset for scrolling effect
        self.background_y = 0  # For scrolling background effect
        self.obstacle_spawn_rate = 30  # Frames between obstacle spawns
        self.collision_played = False  # Track if collision sound was played

    def spawn_obstacle(self):
        if random.randint(1, self.obstacle_spawn_rate) == 1:
            self.obstacles.append(Obstacle())

    def update(self):
        if self.game_over:
            return

        # Update car position (always moving up relative to camera)
        self.car.y -= CAR_SPEED

        # Update obstacles
        for obstacle in self.obstacles:
            obstacle.update()

        # Remove obstacles that are off screen
        self.obstacles = [obs for obs in self.obstacles if not obs.is_off_screen()]

        # Spawn new obstacles
        self.spawn_obstacle()

        # Update score based on how far we've gone
        self.score += 1

        # Check for collisions
        self.check_collisions()

        # Update camera to follow car (keep car centered vertically)
        self.camera_y = self.car.y - (SCREEN_HEIGHT // 2)

        # Keep camera within bounds
        if self.camera_y < 0:
            self.camera_y = 0
        elif self.camera_y > SCREEN_HEIGHT - CAR_HEIGHT:
            self.camera_y = SCREEN_HEIGHT - CAR_HEIGHT

    def check_collisions(self):
        car_rect = pygame.Rect(self.car.x, self.car.y, self.car.width, self.car.height)

        for obstacle in self.obstacles:
            obstacle_rect = pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)
            if car_rect.colliderect(obstacle_rect):
                # Play collision sound if available
                if collision_sound:
                    collision_sound.play()
                self.game_over = True
                break

    def draw(self, screen):
        # Clear screen with a simple background
        screen.fill(WHITE)

        # Draw a simple road (just lines to give illusion of movement)
        road_color = (100, 100, 100)
        lane_color = (200, 200, 200)

        # Draw road background
        pygame.draw.rect(screen, road_color, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        # Draw lane dividers (moving with camera)
        for i in range(1, LANE_COUNT):
            x = i * LANE_WIDTH
            # Draw dashed line for lane divider
            for y in range(0, SCREEN_HEIGHT, 40):
                pygame.draw.line(screen, lane_color, (x, y + self.camera_y), (x, y + 20 + self.camera_y), 3)

        # Draw car (at fixed position on screen)
        car_screen_y = SCREEN_HEIGHT // 2  # Car always appears centered vertically
        screen.blit(car_img, (self.car.x, car_screen_y))

        # Draw obstacles (offset by camera)
        for obstacle in self.obstacles:
            obstacle_screen_y = obstacle.y - self.camera_y
            if 0 <= obstacle_screen_y <= SCREEN_HEIGHT:  # Only draw if on screen
                screen.blit(obstacle_img, (obstacle.x, obstacle_screen_y))

        # Draw score
        score_text = small_font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Draw game over message if needed
        if self.game_over:
            game_over_text = font.render("GAME OVER!", True, RED)
            restart_text = small_font.render("Press R to restart", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
            screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 20))

# Main game function
def main():
    # Initialize game state
    game_state = GameState()

    # Set up clock for FPS control
    clock = pygame.time.Clock()

    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game_state.car.move_left()
                elif event.key == pygame.K_RIGHT:
                    game_state.car.move_right()
                elif event.key == pygame.K_r and game_state.game_over:
                    # Restart game
                    game_state = GameState()

        # Update game state
        game_state.update()

        # Draw everything
        game_state.draw(screen)

        # Update the display
        pygame.display.flip()

        # Control frame rate
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()