# Ethan Lawrence 
# Feb 12 2025
# Pygame template ver 2

import pygame
import sys
import config
import random
import copy

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
        'coords' : [config.WINDOW_WIDTH/2, config.WINDOW_HEIGHT*11/12],
        'speed' : 0,
        'color' : config.GREY,
        'size' : [config.WINDOW_WIDTH/6, config.WINDOW_HEIGHT/50]
    }
    bricks = build_stage()

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
            ball['speed'] = [0, 5]
        # Other collitions
        # collitions : Paddle
        left_object = pygame.Rect(paddle['coords'][0], paddle['coords'][1], paddle['size'][0]/2, paddle['size'][1])
        right_object = pygame.Rect(paddle['coords'][0] + paddle['size'][0]/2, paddle['coords'][1], paddle['size'][0]/2, paddle['size'][1])
        if left_object.collidepoint(ball['coords']):
            ball['speed'][1] *= -1
            ball['speed'][0] *= -1
            ball['speed'][0] -= random.randint(1, 2)
        if right_object.collidepoint(ball['coords']):
            ball['speed'][1] *= -1
            ball['speed'][0] *= -1
            ball['speed'][0] += random.randint(1, 2)
        # collitions : Brick
        del_brick = 0
        for brick in bricks:
            brick_collider = pygame.Rect(brick['coords'][0], brick['coords'][1], brick['size'][0], brick['size'][1])
            if brick_collider.collidepoint(ball['coords']):
                ball['speed'][1] *= -1
                ball['speed'][0] *= -1
                del_brick = brick
        if del_brick != 0:
            bricks.remove(del_brick)
        # - - - Player - - - #
        # Keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            paddle['speed'] -= 0.75
        elif keys[pygame.K_d]:
            paddle['speed'] += 0.75
        # Momentum
        if paddle['speed'] > 0:
            paddle['speed'] -= .5
        elif paddle['speed'] < 0:
            paddle['speed'] += .5
        # Player - Walls
        if not 0 < paddle['coords'][0]:
            paddle['speed'] *= 0.75
            paddle['speed'] += 2
        if not paddle['coords'][0] < config.WINDOW_WIDTH-1 - paddle['size'][0]:
            paddle['speed'] *= 0.75
            paddle['speed'] -= 2
        paddle['coords'][0] += paddle['speed']

        # Draw game
        pygame.draw.circle(screen, ball['color'], ball['coords'], ball['size'])
        pygame.draw.rect(screen, paddle['color'], (paddle['coords'], paddle['size']), border_radius=10)
        for drawing in bricks:
            pygame.draw.rect(screen, drawing['color'], (drawing['coords'], drawing['size']), border_radius=5)
        # Limit clock to FPS & Update Screen
        pygame.display.flip()
        clock.tick(config.FPS)
    pygame.quit()
    sys.exit()

# Other Functions
def build_stage():
    brick_list = []
    building_stage = True
    brick_width = config.WINDOW_WIDTH/(config.COLUMNS+3) # +3 for 1 bricklength on both sides & gaps
    brick_height = config.WINDOW_HEIGHT/(config.ROWS*3) # *3 to have the 2nd half empty
    brick_gap_h = brick_height/ (config.ROWS - 1) # -1 because 1 less gap then blocks
    brick_gap_w = brick_width / (config.COLUMNS - 1) # Gaps total area = 1 brick
    brick_spawn = [-brick_gap_w, brick_gap_h]
    
    while building_stage:
        brick_spawn[0] += brick_width + brick_gap_w
        if brick_spawn[0] > (brick_width*config.COLUMNS)+(brick_gap_w*(config.COLUMNS-1)):
            brick_spawn[1] += brick_height + brick_gap_h
            brick_spawn[0] = brick_width
        if brick_spawn[1] >= (brick_height*config.ROWS)+(brick_gap_h*(config.ROWS-1)):
            building_stage = False
            continue
        brick_list.append(copy.deepcopy({
        'coords' : brick_spawn,
        'color' : (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        'size' : [brick_width, brick_height]
        }))
    return brick_list
    
# Startup
if __name__ == '__main__':
    main()