import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
fps = 60

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

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if not current_direction == 'left':
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

        # Move snake forward
        if event.type == move_event:
            body.pop()
            body.insert(0, body[0].copy())
            if next_direction == "right":
                body[0].x = body[0].x + grid_size
            if next_direction == "left":
                body[0].x = body[0].x - grid_size
            if next_direction == "up":
                body[0].y = body[0].y - grid_size
            if next_direction == "down":
                body[0].y = body[0].y + grid_size
            current_direction = next_direction

            # Check apple collision
            if body[0].colliderect(apple):
                while True:
                    new_x = random.randint(0, (screen.get_width() - grid_size) // grid_size) * grid_size
                    new_y = random.randint(0, (screen.get_height() - grid_size) // grid_size) * grid_size
                    apple = pygame.Rect(new_x, new_y, grid_size, grid_size)

                    if not any(segment.colliderect(apple) for segment in body):
                        break
                    else:
                        print("apple spawned inside snake")
                body.insert(-1, pygame.Rect(body[-1].x, body[-1].y, grid_size, grid_size))

    # Rendering
    screen.fill("black")
    pygame.draw.rect(screen, "red", apple)
    for square in body:
        pygame.draw.rect(screen, "blue", square)
    pygame.draw.rect(screen, "green", body[0])

    # Update Screen
    pygame.display.flip()
    clock.tick(fps)
