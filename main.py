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

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Rendering
    screen.fill("black")
    for square in body:
        pygame.draw.rect(screen, "blue", square)
    pygame.draw.rect(screen, "green", body[0])

    # Update Screen
    pygame.display.flip()
    clock.tick(fps)
