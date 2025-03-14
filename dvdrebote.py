# Que reboti al tocar una paret
import pygame

pygame.init()

# screen
length = pygame.display.Info().current_w
height = pygame.display.Info().current_h
size = (length, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pantalla del joc")

# background color
bg_color = (160, 160, 160)

# creem el logo
logo = pygame.image.load("assets/IMG_20250220_090932.jpg")
logo = pygame.transform.scale(logo, (200, 100))
logo_rect = logo.get_rect()
logo_rect.center = (length // 2, height // 2)

# FPS
FPS = 30
clock = pygame.time.Clock()

# moviment
moviment_x = 5
moviment_y = 5

# Main loop
run = True

while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    # Move the logo
    logo_rect.x += moviment_x
    logo_rect.y += moviment_y

    # Check for collision with the walls
    if logo_rect.right >= length or logo_rect.left <= 0:
        moviment_x = -moviment_x
    if logo_rect.bottom >= height or logo_rect.top <= 0:
        moviment_y = -moviment_y

    screen.fill(bg_color)
    screen.blit(logo, logo_rect)
    pygame.display.flip()

pygame.quit()