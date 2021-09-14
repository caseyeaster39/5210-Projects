import random
import numpy as np


class Robot:
    def __init__(self, episodes):
        # Episode tracking
        self.episode = 0
        self.episodes = episodes

        # Order tracking
        self.orders = []
        self.items = []
        self.complete = False

        # Score tracking
        self.score = 0
        self.max_score = 0
        self.min_score = 0
        self.avg_score = 0

        # Environment navigation
        self.false_positive_rate = 10
        self.false_negative_rate = 10
        self.surroundings = {
            'up':       '*',
            'down':     '*',
            'left':     '*',
            'right':    '*',
        }
        self.moves = {
            'up':       np.array([-1, 0]),
            'down':     np.array([1, 0]),
            'left':     np.array([0, -1]),
            'right':    np.array([0, 1]),
        }
        self.first_lap = [
            'right',
            'down',
            'down',
            'down',
            'down',
            'right',
            'right',
            'right',
            'up',
            'up',
            'up',
            'up',
        ]
        self.forward_path = [
            'down',
            'down',
            'down',
            'down',
            'right',
            'right',
            'right',
            'up',
            'up',
            'up',
            'up',
        ]
        self.back_path = [
            'down',
            'down',
            'down',
            'down',
            'down',
            'left',
            'left',
            'left',
            'up',
            'up',
            'up',
            'up',
            'up',
        ]

        # Position tracking
        self.position = []
        self.current_path = [[0, 0]]
        self.worst_path = []
        self.best_path = []

    def new_episode(self, environment):
        self.orders = order_gen()                                                   # Generate orders
        self.complete = False                                                       # Initialize episode values
        self.items = []
        self.position = np.array([0, 0])
        self.current_path = [[0, 0]]
        self.score = 0
        self.episode += 1

        self.search_pattern(environment, path=self.first_lap)                       # Start first lap

        while not self.complete:                                                    # Continue loop until
            self.search_pattern(environment, path=self.back_path)                       # all items are found
            self.search_pattern(environment, path=self.forward_path)

    def search_pattern(self, environment, path):                                    # Step through environment
        for step in path:                                                           # Path contains "steps"
            self.move(step, environment)                                            # Move method called
            self.look_around(environment)                                           # View surroundings
            self.check_orders(environment)                                          # Check surrounding shelves
            if self.complete:
                break

    def move(self, direction, environment):                                         # Accepts a step (direction)
        self.position += self.moves[direction]                                      # Add step to robot position
        if environment[self.position[0]][self.position[1]] in self.orders:          # Assess score from new position
            self.score += 3
        else:
            self.score -= 1
        self.current_path.append(list(self.position))                               # Store new position

    def look_around(self, environment):                                             # Read from "sensors"
        sensor_position = {
            'up': self.position + self.moves['up'],
            'down': self.position + self.moves['down'],
            'left': self.position + self.moves['left'],
            'right': self.position + self.moves['right']
        }

        self.check_error()                                                          # Error rates from prompt

        for sensor in self.surroundings:
            try:                                                                    # Wall finding, shows empty cell
                if sensor_position[sensor][0] < 0 or sensor_position[sensor][1] < 0:
                    self.surroundings[sensor] = '*'
                else:
                    self.surroundings[sensor] = environment[sensor_position[sensor][0]][sensor_position[sensor][1]]
            except IndexError:
                self.surroundings[sensor] = '*'

    def check_error(self):
        false_pos = random.randint(1, 100)                                          # Generate each type of error
        false_neg = random.randint(1, 100)

        if false_pos <= self.false_positive_rate:                                   # False positive
            self.surroundings[random.choice(list(self.surroundings))] = 'fake'      # Places a random fake "shelf"

        if false_neg <= self.false_negative_rate:                                   # False negative
            self.surroundings[random.choice(list(self.surroundings))] = '*'         # Places a random fake "empty"

    def check_orders(self, environment):
        for item in self.orders:                                                    # If a required item from the
            if item in self.surroundings.values() and item not in self.items:       # order list is adjacent,
                self.retrieve(item, environment)                                    # Retrieve it
        if 'fake' in self.surroundings:                                             # Same process for fake but is
            self.retrieve('fake', environment)                                      # handled in retrieve method

    def retrieve(self, item, environment):
        for direction, shelf in self.surroundings.items():                          # From surroundings,
            if shelf == item:                                                       # find shelf containing target
                if item != 'fake':                                                  # For real items,
                    self.move(direction, environment)                               # move to shelf,
                    self.items.append(item)                                         # grab item,
                    if self.check_complete():                                       # check if orders completed
                        self.finish_episode()                                       # finish episode if completed
                    else:
                        back = direction_flip(direction)                            # otherwise, move back
                        self.move(back, environment)
                else:
                    fake_shelf = random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'])

                    if fake_shelf in self.orders and fake_shelf not in self.items:  # If the fake is a target shelf,
                        self.move(direction, environment)                           # try and fail to get the item
                        back = direction * -1
                        self.move(back, environment)

    def check_complete(self):
        for item in self.orders:                                                    # Check order list
            if item not in self.items:                                              # If an order has not yet been added
                return False                                                        # not complete.
        return True                                                                 # If all items are found, complete.

    def finish_episode(self):                                                       # Update metrics
        self.avg_score = (self.avg_score * (self.episode - 1) + self.score) / self.episode
        if self.episode == 1:                                                       # Initial values after episode 1
            self.max_score = self.score
            self.min_score = self.score
            self.best_path = self.current_path
            self.worst_path = self.current_path
        else:                                                                       # Update values if needed
            if self.score > self.max_score:                                         # Best score and path
                self.max_score = self.score
                self.best_path = self.current_path
            if self.score < self.min_score:                                         # Worst score and path
                self.min_score = self.score
                self.worst_path = self.best_path
        self.complete = True


def map_initialize():
    cord_dict = {
        'A': [1, 1],
        'B': [2, 2],
        'C': [1, 3],
        'D': [2, 0],
        'E': [0, 2],
        'F': [2, 4],
        'G': [4, 1],
        'H': [5, 4],
        'J': [3, 5],
        'I': [4, 2]
    }
    empty_arr = np.array([['*' for i in range(6)] for j in range(6)])

    # Each time loop runs "letter is different key from dict.
    for letter, (x_pos, y_pos) in cord_dict.items():    # "letter" represents key of dictionary.
        empty_arr[y_pos][x_pos] = letter                # Key Value ("letter") is placed into empty_arr using x and y

    return empty_arr


def order_gen():
    orders = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']                     # Possible orders
    random.shuffle(orders)                                                          # Shuffle order of orders
    order_set = [orders[x] for x in range(random.randint(1, 10))]                   # Random orders (1-10 in total)
    return order_set


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


def report_printout(robot):
    print('\n##############################\n')
    print(f'Average Score: {robot.avg_score}')                                      # Print results
    print(f'Maximum Score: {robot.max_score}')
    print(f'Minimum Score: {robot.min_score}')

    baseline_score = 4 * len(robot.orders) - 35                                     # Brute force score,
    print(f'\nBaseline Score: {baseline_score}')                                    # per Dr. Pears
    print('\n##############################\n')


def main():                                                                         # Main function
    environment = map_initialize()                                                  # Create map
    robot = Robot(1000)                                                             # Initialize robot

    for i in range(robot.episodes):                                                 # Perform episodes
        robot.new_episode(environment)                                              # Start new episode

    report_printout(robot)


if __name__ == '__main__':                                                          # Python best practices
    main()
