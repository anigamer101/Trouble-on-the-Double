import pygame
import sys

pygame.init()

info = pygame.display.Info()
w = info.current_w
h = info.current_h

icon = pygame.image.load('assets/imgs/logo/LOGO.png')

# Set up the display
window = pygame.display.set_mode(
    (w, h),
    pygame.DOUBLEBUF
)
pygame.display.set_icon(icon)
pygame.display.set_caption("Trouble on the Double")

# Initial positions of the rectangles
rect_x, rect_y = 100, 100  # Blue player
circx, circy = 400, 400    # Red player (start far to test collision!)

# Font for displaying text
font = pygame.font.Font(None, 50)

# Clock to control the frame rate
clock = pygame.time.Clock()

# Game state
game_state = "running"

# Load sounds
win_sound = pygame.mixer.Sound(r"assets\sfx\win.wav")
tie_sound = pygame.mixer.Sound(r"assets\sfx\game_over.wav")
level_sound = pygame.mixer.Sound(r"assets\sfx\level.wav")

# Play background sound (looped)
level_sound.play(-1)

# Load images and background
image = pygame.image.load(r"assets\imgs\costume.png").convert_alpha()
image = pygame.transform.scale(image, (90, 90))

image2 = pygame.image.load(r"assets\imgs\costume1.png").convert_alpha()
image2 = pygame.transform.scale(image2, (90, 90))

bg = pygame.image.load(r"assets\imgs\court.png").convert_alpha()
bg = pygame.transform.scale(bg, (w, h))

# Precompute masks from surfaces
mask1 = pygame.mask.from_surface(image)
mask2 = pygame.mask.from_surface(image2)

# Helper to reset positions
def reset_positions():
    global rect_x, rect_y, circx, circy
    rect_x, rect_y = 100, 100
    circx, circy = 400, 400

# Button function
def draw_button(surface, color, rect, text, text_color=(0, 0, 0)):
    pygame.draw.rect(surface, color, rect, border_radius=8)
    button_text = font.render(text, True, text_color)
    text_rect = button_text.get_rect(center=rect.center)
    surface.blit(button_text, text_rect)

# Define buttons
exit_button_rect = pygame.Rect(800, 700, 200, 50)

# Main loop
running = True
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # If the exit button was clicked
            if exit_button_rect.collidepoint(mouse_pos):
                running = False
                pygame.quit()
                sys.exit()

    # Handle movement if the game is still running
    if game_state == "running":
        keys = pygame.key.get_pressed()

        # Move the blue sprite (WASD)
        if keys[pygame.K_w]:
            rect_y -= 5
        if keys[pygame.K_s]:
            rect_y += 5
        if keys[pygame.K_a]:
            rect_x -= 5
        if keys[pygame.K_d]:
            rect_x += 5

        # Move the red sprite (Arrow keys)
        if keys[pygame.K_UP]:
            circy -= 5
        if keys[pygame.K_DOWN]:
            circy += 5
        if keys[pygame.K_LEFT]:
            circx -= 5
        if keys[pygame.K_RIGHT]:
            circx += 5

        # Calculate offset FROM mask1 TO mask2
        offset = (circx - rect_x, circy - rect_y)

        # Collision detection
        overlap = mask1.overlap(mask2, offset)

        if overlap:
            if keys[pygame.K_SPACE] and not keys[pygame.K_RCTRL]:
                game_state = "blue_wins"
            elif keys[pygame.K_RCTRL] and not keys[pygame.K_SPACE]:
                game_state = "red_wins"
            elif keys[pygame.K_RCTRL] and keys[pygame.K_SPACE]:
                game_state = "tie"
            else:
                game_state = "tie"

    # Draw everything
    window.fill((255, 255, 255))
    window.blit(bg, (0, 0))

    # Draw both players during gameplay
    if game_state == "running":
        window.blit(image, (rect_x, rect_y))
        window.blit(image2, (circx, circy))

    # Handle end states
    if game_state == "blue_wins":
        text_surface = font.render("BLUE WINS", True, (0, 0, 255))
        text_rect = text_surface.get_rect(center=(514, 400))
        window.blit(text_surface, text_rect)

        win_sound.play()
        pygame.display.flip()
        pygame.time.delay(2000)

        reset_positions()
        game_state = "running"

    elif game_state == "red_wins":
        text_surface = font.render("RED WINS", True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(514, 400))
        window.blit(text_surface, text_rect)

        win_sound.play()
        pygame.display.flip()
        pygame.time.delay(2000)

        reset_positions()
        game_state = "running"

    elif game_state == "tie":
        text_surface = font.render("TIE", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(514, 400))
        window.blit(text_surface, text_rect)

        tie_sound.play()
        pygame.display.flip()
        pygame.time.delay(2000)

        reset_positions()
        game_state = "running"

    # Draw exit button in all game states!
    mouse_pos = pygame.mouse.get_pos()
    if exit_button_rect.collidepoint(mouse_pos):
        button_color = (200, 0, 0)  # Hover color
    else:
        button_color = (150, 0, 0)  # Normal color
    draw_button(window, button_color, exit_button_rect, "EXIT", text_color=(255, 255, 255))

    # Update display
    pygame.display.flip()

    # Frame rate
    clock.tick(30)

pygame.quit()
