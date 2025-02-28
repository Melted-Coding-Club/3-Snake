import pygame

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

next_direction = "right"

move_event = pygame.USEREVENT + 1
pygame.time.set_timer(move_event, 250)

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

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

    # Rendering
    screen.fill("black")
    for square in body:
        pygame.draw.rect(screen, "blue", square)
    pygame.draw.rect(screen, "green", body[0])

    # Update Screen
    pygame.display.flip()
    clock.tick(fps)
