import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
font = pygame.font.SysFont("Segoe UI", 35)
fps = 60

grid_size = 40

current_direction = "right"
next_direction = "right"

move_event = pygame.USEREVENT + 1
pygame.time.set_timer(move_event, 250)

# Initialize snake and apple
apple = pygame.Rect(grid_size * 5, grid_size * 5, grid_size, grid_size)
body = [
    pygame.Rect(grid_size * 5, grid_size * 5, grid_size, grid_size),
    pygame.Rect(grid_size * 4, grid_size * 5, grid_size, grid_size),
]


def render():
    """ Draws the game elements on the screen. """
    screen.fill("dark gray")
    pygame.draw.rect(screen, "red", apple)

    for square in body:
        pygame.draw.rect(screen, "blue", square)

    pygame.draw.rect(screen, "green", body[0])

    text_surface = font.render(f"Length: {len(body)}", False, "white")
    screen.blit(text_surface, (2, 2))

    if is_over:
        game_over_text = font.render("Game Over - Press SPACE to Restart", False, "red")
        screen.blit(game_over_text, (
            screen.get_width() // 2 - game_over_text.get_width() // 2,
            screen.get_height() // 2 - game_over_text.get_height() // 2
        ))

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
                # Reset game state
                body = [
                    pygame.Rect(grid_size * 5, grid_size * 5, grid_size, grid_size),
                    pygame.Rect(grid_size * 4, grid_size * 5, grid_size, grid_size),
                ]
                current_direction = "right"
                next_direction = "right"
                is_over = False

        render()
        continue

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and current_direction != 'left':
                next_direction = "right"
            elif event.key == pygame.K_LEFT and current_direction != 'right':
                next_direction = "left"
            elif event.key == pygame.K_UP and current_direction != 'down':
                next_direction = "up"
            elif event.key == pygame.K_DOWN and current_direction != 'up':
                next_direction = "down"

        if event.type == move_event:
            # Move snake forward
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

            # Check apple collision
            if body[0].colliderect(apple):
                while True:
                    new_x = random.randint(0, (screen.get_width() - grid_size) // grid_size) * grid_size
                    new_y = random.randint(0, (screen.get_height() - grid_size) // grid_size) * grid_size
                    new_apple = pygame.Rect(new_x, new_y, grid_size, grid_size)

                    if not any(segment.colliderect(new_apple) for segment in body):
                        apple = new_apple
                        break
            else:
                body.pop()  # Remove last segment if no apple eaten

            # Check snake collision with walls
            if body[0].right > screen.get_width() or body[0].left < 0 or body[0].top < 0 or body[0].bottom > screen.get_height():
                is_over = True
                break

            # Check self-collision
            for segment in body[1:]:
                if body[0].colliderect(segment):
                    is_over = True
                    break

    render()
