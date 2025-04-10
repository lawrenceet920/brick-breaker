# Ethan Lawrence 
# Feb 12 2025
# Pygame template ver 2

import pygame
import sys
import config

# Generic Functions
def init_game():
    pygame.init()
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    pygame.display.set_caption(config.TITLE)
    return screen
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
    return True
def main():
    screen = init_game()
    clock = pygame.time.Clock()
    running = True
    # On Startup
    ball = {
        'coords' : [config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2],
        'speed' : [0, 5],
        'color' : config.BLACK,
        'size' : 5
    }
    paddle = {
        'coords' : [config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT-50],
        'speed' : 0,
        'color' : config.BLACK,
        'size' : [config.WINDOW_WIDTH/6, config.WINDOW_HEIGHT/50]
    }
    while running:
        running = handle_events()
        screen.fill(config.WHITE)
        # While Running
        # - - - Ball - - - #
        ball['coords'][0] += ball['speed'][0]
        ball['coords'][1] += ball['speed'][1]
        if not (0 < ball['coords'][0] < config.WINDOW_WIDTH-1 - ball['size']):
                ball['speed'][0] *= -1
        if not (0 < ball['coords'][1]):
            ball['speed'][1] *= -1
        # Fall down
        if  ball['coords'][1] > config.WINDOW_HEIGHT:
            ball['coords'] = [config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT/2]
        # Other collitions
        this_object = pygame.Rect(paddle['coords'][0], paddle['coords'][1], paddle['size'], paddle['size'])
        if this_object.collidepoint(ball['coords']):
            ball['speed'][1] *= -1
            ball['speed'][0] *= -1

        # - - - Player - - - #
        # Keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            paddle['speed'] -= 0.25
        elif keys[pygame.K_d]:
            paddle['speed'] += 0.25
        else: # Momentum
            if paddle['speed'] > 0:
                paddle['speed'] -= .5
            elif paddle['speed'] < 0:
                paddle['speed'] += .5
        # Player - Walls
        if not 0 < paddle['coords'][0]:
            paddle['speed'] += 2
        if not paddle['coords'][0] < config.WINDOW_WIDTH-1 - paddle['size'][0]:
            paddle['speed'] -= 2
        paddle['coords'][0] += paddle['speed']

        # Draw game
        pygame.draw.circle(screen, ball['color'], ball['coords'], ball['size'])
        pygame.draw.rect(screen, paddle['color'], (paddle['coords'], paddle['size']), border_radius=10)
        # Limit clock to FPS & Update Screen
        pygame.display.flip()
        clock.tick(config.FPS)
    pygame.quit()
    sys.exit()

# Other Functions

# Startup
if __name__ == '__main__':
    main()