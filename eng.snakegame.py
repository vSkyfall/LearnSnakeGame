import pygame, sys, random

# Screen dimensions
screen_width = 600
screen_height = 600

# Background grid size and cell dimensions
gridsize = 20
gridwith = screen_width / gridsize  # Number of grid columns
grid_height = screen_height / gridsize  # Number of grid rows

# Color definitions
light_green = (0, 170, 140)  # Light green for grid
dark_green = (0, 140, 120)   # Dark green for grid
food_color = (250, 200, 0)   # Food color
snake_color = (128, 0, 128)  # Snake color (purple)

# Snake movement directions
up = (0, -1)    # Move up
down = (0, 1)   # Move down
right = (1, 0)  # Move right
left = (-1, 0)  # Move left

# High score variable
high_score = 0  # Keeps track of the highest score during the game

# Snake class
class SNAKE:
    def __init__(self):
        self.positions = [((screen_width / 2), (screen_height / 2))]  # Snake starts at the center
        self.lenght = 1  # Initial length of the snake
        self.direction = random.choice([up, down, right, left])  # Random starting direction
        self.color = snake_color  # Snake's color
        self.score = 0  # Player's score

    def draw(self, surface):
        # Draw the snake based on its positions
        for p in self.positions:
            rect = pygame.Rect((p[0], p[1]), (gridsize, gridsize))  # Each segment is a rectangle
            pygame.draw.rect(surface, self.color, rect)

    def move(self):
        # Move the snake
        cur = self.positions[0]  # Snake's head
        x, y = self.direction  # Current direction
        # New head position
        new = (((cur[0] + (x * gridsize)) % screen_width), (cur[1] + (y * gridsize)) % screen_height)
        # If the snake collides with itself
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()  # Reset the snake
            return True  # Notify collision
        else:
            # Update the snake's positions
            self.positions = [new] + self.positions
            if len(self.positions) > self.lenght:  # If the snake didn't grow, remove the tail
                self.positions.pop()
            return False

    def handle_keys(self):
        # Keyboard controls for changing direction
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.direction != down:  # Cannot move down if moving up
            self.direction = up
        elif keys[pygame.K_DOWN] and self.direction != up:  # Cannot move up if moving down
            self.direction = down
        elif keys[pygame.K_RIGHT] and self.direction != left:  # Cannot move left if moving right
            self.direction = right
        elif keys[pygame.K_LEFT] and self.direction != right:  # Cannot move right if moving left
            self.direction = left

    def reset(self):
        # Reset the snake when it dies
        global high_score
        high_score = max(high_score, self.score)  # Update the high score
        self.positions = [((screen_width / 2), (screen_height / 2))]  # Reset position to center
        self.lenght = 1  # Reset length
        self.direction = random.choice([up, down, right, left])  # Randomize direction
        self.score = 0  # Reset score

# Food class
class FOOD:
    def __init__(self):
        self.position = (0, 0)  # Initial position
        self.color = food_color  # Food color
        self.randomize_position()  # Set a random position

    def randomize_position(self):
        # Set food to a random position
        self.position = (random.randint(0, gridwith - 1) * gridsize, random.randint(0, grid_height - 1) * gridsize)

    def draw(self, surface):
        # Draw the food
        rect = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, rect)

# Draw grid
def drawGrid(surface):
    # Draw the background grid
    for y in range(0, int(grid_height)):
        for x in range(0, int(gridwith)):
            if (x + y) % 2 == 0:
                light = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, light_green, light)  # Light green squares
            else:
                dark = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, dark_green, dark)  # Dark green squares
def main_menu():
    # Create the main menu
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    font = pygame.font.SysFont("arial", 40)  # Font for menu text
    clock = pygame.time.Clock()
    while True:
        screen.fill((0, 0, 0))  # Black background
        title_text = font.render("Snake Game", True, (255, 255, 255))  # Game title
        start_text = font.render("1. Start Game", True, (0, 255, 0))  # Start game option
        exit_text = font.render("2. Exit", True, (255, 0, 0))  # Exit option
        # Render text to the screen
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 100))
        screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, 200))
        screen.blit(exit_text, (screen_width // 2 - exit_text.get_width() // 2, 300))
        pygame.display.update()
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Press "1" to start the game
                    return
                elif event.key == pygame.K_2:  # Press "2" to exit
                    pygame.quit()
                    sys.exit()
        clock.tick(15)  # Limit FPS


def main():
    # Main game loop
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    font = pygame.font.SysFont("arial", 20)  # Font for score text
    clock = pygame.time.Clock()
    surface = pygame.Surface(screen.get_size())  # Main surface
    surface = surface.convert()
    snake = SNAKE()  # Create snake instance
    food = FOOD()  # Create food instance

    global high_score  # High score as a global variable
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Game logic
        clock.tick(15)  # Limit FPS
        snake.handle_keys()  # Handle player input
        collision = snake.move()  # Move the snake and check for collisions
        if collision:
            # If the snake dies, show death menu
            death_menu(screen, snake.score)
            return

        if snake.positions[0] == food.position:
            # If the snake eats the food
            snake.lenght += 1
            snake.score += 1
            food.randomize_position()

        # Render score texts
        score_text = font.render("Score: " + str(snake.score), True, (255, 255, 255))
        high_score_text = font.render("High Score: " + str(high_score), True, (255, 255, 255))

        # Clear surface and draw elements
        surface.fill((0, 0, 0))
        drawGrid(surface)  # Draw the grid
        food.draw(surface)  # Draw the food
        snake.draw(surface)  # Draw the snake
        surface.blit(score_text, (10, 10))  # Display current score
        surface.blit(high_score_text, (10, 40))  # Display high score
        screen.blit(surface, (0, 0))
        pygame.display.update()


def death_menu(screen, score):
    # Create the death menu
    font = pygame.font.SysFont("arial", 40)  # Font for menu text
    clock = pygame.time.Clock()
    while True:
        screen.fill((0, 0, 0))  # Black background
        death_text = font.render("Game Over", True, (255, 0, 0))  # Game over message
        score_text = font.render(f"Your Score: {score}", True, (255, 255, 255))  # Display player's score
        restart_text = font.render("1. Restart", True, (0, 255, 0))  # Restart option
        exit_text = font.render("2. Exit", True, (255, 0, 0))  # Exit option
        # Render text to the screen
        screen.blit(death_text, (screen_width // 2 - death_text.get_width() // 2, 100))
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 200))
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, 300))
        screen.blit(exit_text, (screen_width // 2 - exit_text.get_width() // 2, 400))
        pygame.display.update()
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Press "1" to restart
                    return
                elif event.key == pygame.K_2:  # Press "2" to exit
                    pygame.quit()
                    sys.exit()
        clock.tick(15)  # Limit FPS

# Start the game
main_menu()  # Show the main menu
main()  # Start the main game loop
