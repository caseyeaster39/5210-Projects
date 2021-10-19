import pygame
import sys

import warehouse as wh

from pygame.locals import *

# Globals:
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GRAY = (100, 100, 100)
GREEN = (47, 237, 155)
RED = (224, 80, 61)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600

BLOCK_SIZE = int(WINDOW_WIDTH / 6)                                                      # Set the size of the grid block
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))                         # Prepare screen object


def display_results(robot):
    pygame.init()                                                                       # Pygame initialize
    for window in [0, 1]:                                                               # For best and worst paths
        screen_change = True

        # Window title info
        info = ', press any key to continue...'
        caption = f'Best Score: {robot.max_path}{info}' if window == 0 else f'Worst Score: {robot.min_path}{info}'
        pygame.display.set_caption(f'{caption}')

        # More setup
        SCREEN.fill(BLACK)
        font = pygame.font.SysFont(name='arial', size=20)

        # My stuff
        draw_grid()                                                                     # Draw grid
        draw_shelves(font, robot.warehouse)                                             # Draw warehouse layout
        path = robot.best_path if window == 0 else robot.worst_path                     # Pick path to display,
        draw_path(path)                                                                 # and draw said path.

        # Typical pygame loop
        while screen_change:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:                                               # Next screen
                    screen_change = False

            pygame.display.update()


def draw_shelves(font, warehouse):
    environment = wh.map_initialize(warehouse)                                          # To be displayed
    for i in range(len(environment)):
        for j in range(len(environment[0])):
            cell = environment[i][j]                                                    # Get each value
            color = GRAY if cell == '*' else GREEN                                      # Shelves are green
            img = font.render(cell, True, color)                                        # Render text
            x = (j + .25) * BLOCK_SIZE                                                  # Position to display
            y = (i + .25) * BLOCK_SIZE
            SCREEN.blit(img, (x, y))                                                    # Place on screen object


def draw_path(path):
    last_coord = [.5 * BLOCK_SIZE, .5 * BLOCK_SIZE]                                     # Start from origin
    for coord in path:
        next_coord = [(coord[1] + .5) * BLOCK_SIZE, (coord[0] + .5) * BLOCK_SIZE]       # Get endpoint
        pygame.draw.line(SCREEN, RED, last_coord, next_coord, width=5)                  # Draw line from last to next
        last_coord = next_coord                                                         # Current becomes last point


def draw_grid():                                                                        # Draw grid
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)


def report_printout(robot):
    print('\n##############################\n')
    print(f'Average Score: {round(robot.avg_score, 3)}')                                # Print results
    print(f'Avg. Brute Force Score: {round(robot.baseline_score_avg, 3)}\n')

    print(f'Maximum Score: {robot.max_path}')
    print(f'Corresponding Brute Force Score: {robot.baseline_score_max}\n')

    print(f'Minimum Score: {robot.min_path}')
    print(f'Corresponding Brute Force Score: {robot.baseline_score_min}')
    print('\n##############################\n')

    display_results(robot)                                                              # Display paths


def direction_flip(direction):                                                          # Ugly solution
    if direction == 'up':
        return 'down'
    elif direction == 'down':
        return 'up'
    elif direction == 'left':
        return 'right'
    elif direction == 'right':
        return 'left'
    else:
        return None
