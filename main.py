import random
import sys
import pygame
import copy

# Boiler plate code for pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont("Segoe UI", 35)

grid_size = 40
# Creates head variable as a Rect object which we will move around the screen.
head = pygame.Rect(grid_size * 5, grid_size * 5, grid_size, grid_size)

# Creates a body list which has Rect objects within it. 
# This allows us to easily add more bodies to the list to extend the snake. **This is an important idea**
body = [
    pygame.Rect(grid_size * 4, grid_size * 5, grid_size, grid_size),
]
# Direction variable allows the snake to travel in a direction different to the user input
direction = None

# Creates a Rect object to represent the apple
apple = pygame.Rect(grid_size * 3, grid_size * 3, grid_size, grid_size)

# Create a custom event which is added to the event loop every 0.25 seconds
move_event = pygame.USEREVENT + 1
pygame.time.set_timer(move_event, 250)

# Create a variable to keep track of whether the snake is alive or dead
isAlive = True

# Create the main game loop
while True:
    # Run the event code for every event in the pygame.event.get() list
    for event in pygame.event.get():
        # Filter the event type, if is clicking the red X, quit the game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # If the event is a KEYDOWN and the snake is still alive.
        # This is because if the snake is dead, we dont need to worry about it's direction.
        if event.type == pygame.KEYDOWN and isAlive:
            # Filter keys the arrow keys. 
            if event.key == pygame.K_RIGHT:
                # Make sure the snake isnt heading in the opposite direction.
                if not direction == 'left':
                    # Update the direction variable.
                    direction = "right"
            if event.key == pygame.K_LEFT:
                if not direction == 'right':
                    direction = "left"
            if event.key == pygame.K_UP:
                if not direction == 'down':
                    direction = "up"
            if event.key == pygame.K_DOWN:
                if not direction == 'up':
                    direction = "down"
            
            # This is debug code or just a fun addition.
            # If the SPACE key is pressed, it increases the length of the snake by adding an extra body to it
            if event.key == pygame.K_SPACE:
                body.insert(-1, pygame.Rect(body[-1].x, body[-1].y, grid_size, grid_size))

        # If the event is a KEYDOWN and the snake is still **not** alive.
        # This will handle the events while the snake is dead
        elif event.type == pygame.KEYDOWN and not isAlive:
            # If the SPACE key is pressed
            if event.key == pygame.K_SPACE:
                # Reset game
                head = pygame.Rect(grid_size * 5, grid_size * 5, grid_size, grid_size)
                body = [
                    pygame.Rect(grid_size * 4, grid_size * 5, grid_size, grid_size)
                ]
                direction = None
                isAlive = True

        # If the event is a move_event and the snake is alive.
        # This allows the snake to move at a set rate and if the snake is dead, we do not need to calculate any movement
        if event.type == move_event and isAlive:
            # Filter by direction
            if direction == "right":
                # Add a copy of the head to body
                body.insert(0, copy.copy(head))
                head.x = head.x + grid_size
            if direction == "left":
                body.insert(0, copy.copy(head))
                head.x = head.x - grid_size
            if direction == "up":
                body.insert(0, copy.copy(head))
                head.y = head.y - grid_size
            if direction == "down":
                body.insert(0, copy.copy(head))
                head.y = head.y + grid_size

            # Check collision between the head of the snake and the apple
            if head.colliderect(apple):
                apple.x = random.randint(0, (screen.get_width() - grid_size) // grid_size) * grid_size
                apple.y = random.randint(0, (screen.get_height() - grid_size) // grid_size) * grid_size
                body.insert(-1, pygame.Rect(body[-1].x, body[-1].y, grid_size, grid_size))

            # Chech whether the head has gon off screem
            if head.right > (screen.get_width()) or head.left < 0:
                # Switch to the dead state
                isAlive = False
            if head.top < 0 or head.bottom > (screen.get_height()):
                isAlive = False

            # Loop through each segment in the snake's body
            for segment in body:
                # Check for Collisions with the body
                if head.colliderect(segment):
                    isAlive = False

            # If moving, remove the last segment
            if direction:
                body.pop()
    
    # This is the rendering part of the code. Things rendered first can be drawn over by things rendered after them. 
    # This is the required rendering order for each frame:
    # 1. Fill the screen surface with your background colour
    # 2. Draw your game elements, things you want to be drawn on top should be drawn last
    # 3. Update the screen surface with pygame.display.update()

    # Rendering every frame
    screen.fill((64, 64, 64))

    # Draws the apple to the screen
    pygame.draw.rect(screen, "red", apple)

    # Draws each rect in the body list to the screen
    for square in body:
        pygame.draw.rect(screen, "blue", square)
    # Draws the head Rect to the screen
    pygame.draw.rect(screen, "blue", head)

    # Draw the score
    textsurface = font.render(f"Length: {int(len(body) + 1)}", False, "white")  # "text", antialias, color
    screen.blit(textsurface, (2, 2))

    # Draw the game over text if the snake is not alive
    if not isAlive:
        textsurface = font.render("GAME OVER", False, "red")  # "text", antialias, color
        screen.blit(textsurface, (200, 200))

    # Update the screen
    pygame.display.update()
