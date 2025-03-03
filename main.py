import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
fps = 60

grid_size = 40

next_direction = "right"

move_event = pygame.USEREVENT + 1
pygame.time.set_timer(move_event, 250)

body = [
    pygame.Rect(grid_size * 5, grid_size * 5, grid_size, grid_size),
    pygame.Rect(grid_size * 4, grid_size * 5, grid_size, grid_size),
]

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # Player controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                next_direction = "right"
            if event.key == pygame.K_LEFT:
                next_direction = "left"
            if event.key == pygame.K_UP:
                next_direction = "up"
            if event.key == pygame.K_DOWN:
                next_direction = "down"

            if event.key == pygame.K_SPACE:
                body.insert(-1, pygame.Rect(body[-1].x, body[-1].y, grid_size, grid_size))

        if event.type == move_event:
            # Move snake forward
            body.pop()
            body.insert(0, body[0].copy())
            if next_direction == "right":
                body[0].x += grid_size
            elif next_direction == "left":
                body[0].x -= grid_size
            elif next_direction == "up":
                body[0].y -= grid_size
            elif next_direction == "down":
                body[0].y += grid_size
            current_direction = next_direction

    # Rendering
    screen.fill("black")
    for square in body:
        pygame.draw.rect(screen, "blue", square)
    pygame.draw.rect(screen, "green", body[0])

    # Update Screen
    pygame.display.flip()
    clock.tick(fps)
