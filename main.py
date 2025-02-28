import random
import sys
import pygame
import copy

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
fps = 60
font = pygame.font.SysFont("Segoe UI", 35)

grid_size = 40

body = [
    pygame.Rect(grid_size * 5, grid_size * 5, grid_size, grid_size),
    pygame.Rect(grid_size * 4, grid_size * 5, grid_size, grid_size),
]
apple = pygame.Rect(grid_size * 3, grid_size * 3, grid_size, grid_size)

current_direction = "right"
next_direction = "right"

move_event = pygame.USEREVENT + 1
pygame.time.set_timer(move_event, 250)


def render():
    # Rendering
    screen.fill("dark gray")
    pygame.draw.rect(screen, "red", apple)
    for square in body:
        pygame.draw.rect(screen, "blue", square)
    pygame.draw.rect(screen, "green", body[0])

    # Draw the score
    text_surface = font.render(f"Length: {int(len(body))}", False, "white")  # "text", antialias, color
    screen.blit(text_surface, (2, 2))

    if is_over:
        text_surface = font.render("Game Over", False, "red")  # "text", antialias, color
        screen.blit(text_surface, (screen.get_width() // 2 - text_surface.get_width() // 2, screen.get_height() // 2 - text_surface.get_height() // 2))

    # Update the screen
    pygame.display.update()
    clock.tick(fps)


is_over = False
while True:
    if is_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Reset game
                body = [
                    pygame.Rect(grid_size * 5, grid_size * 5, grid_size, grid_size),
                    pygame.Rect(grid_size * 4, grid_size * 5, grid_size, grid_size)
                ]
                direction = None
                is_over = False

        render()
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            # Filter keys the arrow keys. 
            if event.key == pygame.K_RIGHT:
                # Make sure the snake isnt heading in the opposite direction.
                if not current_direction == 'left':
                    # Update the direction variable.
                    next_direction = "right"
            if event.key == pygame.K_LEFT:
                if not current_direction == 'right':
                    next_direction = "left"
            if event.key == pygame.K_UP:
                if not current_direction == 'down':
                    next_direction = "up"
            if event.key == pygame.K_DOWN:
                if not current_direction == 'up':
                    next_direction = "down"
            
            if event.key == pygame.K_SPACE:
                body.insert(-1, pygame.Rect(body[-1].x, body[-1].y, grid_size, grid_size))

        if event.type == move_event:
            body.pop()
            body.insert(0, copy.copy(body[0]))
            if next_direction == "right":
                # Add a copy of the head to body
                body[0].x = body[0].x + grid_size
            if next_direction == "left":
                body[0].x = body[0].x - grid_size
            if next_direction == "up":
                body[0].y = body[0].y - grid_size
            if next_direction == "down":
                body[0].y = body[0].y + grid_size
            current_direction = next_direction

            # Check collision between the head of the snake and the apple
            if body[0].colliderect(apple):
                while True:
                    new_x = random.randint(0, (screen.get_width() - grid_size) // grid_size) * grid_size
                    new_y = random.randint(0, (screen.get_height() - grid_size) // grid_size) * grid_size
                    apple = pygame.Rect(new_x, new_y, grid_size, grid_size)

                    # Ensure apple doesn't spawn inside the snake
                    if not any(segment.colliderect(apple) for segment in body):
                        break
                    else:
                        print("apple spawned inside snake")
                body.insert(-1, pygame.Rect(body[-1].x, body[-1].y, grid_size, grid_size))

            # Check whether the head has gon off screem
            if body[0].right > (screen.get_width()) or body[0].left < 0 or body[0].top < 0 or body[0].bottom > (screen.get_height()):
                # Switch to the dead state
                body.pop(0)
                is_over = True
                break

            # Loop through each segment in the snake's body (excluding the head)
            for i in range(1, len(body)):
                # Check if the head collides with any body segment
                if body[0].colliderect(body[i]):
                    is_over = True
                    break  # Exit loop early if collision is detected

    render()
