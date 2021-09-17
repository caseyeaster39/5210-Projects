

def report_printout(robot):
    print('\n##############################\n')
    print(f'Average Score: {robot.avg_score}')                                      # Print results
    print(f'Maximum Score: {robot.max_score}')
    print(f'Minimum Score: {robot.min_score}')

    baseline_score = 4 * len(robot.orders) - 35                                     # Brute force score,
    print(f'\nBaseline Score: {baseline_score}')                                    # per Dr. Pears
    print('\n##############################\n')


def direction_flip(direction):                                                      # Ugly fix
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
