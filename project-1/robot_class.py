import project_utils
import random

import warehouse as wh
import numpy as np


class Robot:
    def __init__(self, episodes, protocol, layout):
        # Episode tracking
        self.episode = 0
        self.episodes = episodes

        # Order tracking
        self.warehouse = layout
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
        self.protocol = protocol
        self.adjacent = False
        self.next_dir = 'none'
        self.moves = {
            'up':       np.array([-1, 0]),
            'down':     np.array([1, 0]),
            'left':     np.array([0, -1]),
            'right':    np.array([0, 1]),
        }

        # Paths for path protocol (experimental)
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
        self.environment = [[]]
        self.position = []
        self.current_path = [[0, 0]]
        self.worst_path = []
        self.best_path = []

    def start_procedure(self):
        for i in range(self.episodes):                                              # Perform episodes
            self.new_episode()                                                      # Start new episode

    def new_episode(self):
        self.orders = wh.order_gen(self.warehouse)                                  # Generate orders
        self.complete = False                                                       # Initialize episode values
        self.items = []
        self.position = np.array([0, 0])
        self.current_path = [[0, 0]]
        self.score = 0
        self.episode += 1

        self.environment = wh.map_initialize(self.warehouse)                        # Create map

        self.movement_protocol(self.environment)

    def movement_protocol(self, environment):
        if self.protocol == 'path':                                                 # For path protocol:
            self.search_pattern(environment, path=self.first_lap)                   # Start first lap
            while not self.complete:                                                # Continue loop until
                self.search_pattern(environment, path=self.back_path)               # all items are found
                self.search_pattern(environment, path=self.forward_path)
        elif self.protocol == 'random':                                             # For random protocol:
            self.search_pattern(environment)                                        # no path is passed to search

    def search_pattern(self, environment, path=None):                               # Step through environment
        if path:
            for step in path:                                                       # Path contains "steps"
                self.move(step, environment)                                        # Move method called
                self.look_around(environment)                                       # View surroundings
                self.check_orders(environment)                                      # Check surrounding shelves
                if self.complete:
                    break
        else:
            move_options = list(self.moves.keys())                                  # Up, Down, Left, Right
            while not self.complete:                                                # Until all items are found:
                self.adjacent = False                                               # Robot hasn't sensed a target
                self.next_dir = 'none'                                              # Robot hasn't decided a direction
                self.look_around(environment)                                       # View surroundings
                self.check_orders(environment)                                      # Check surrounding shelves

                if self.adjacent:                                                   # If a target is identified,
                    self.move(self.next_dir, environment)                           # move to the target,
                    self.items.append(environment[self.position[0]][self.position[1]])  # pick up target,
                    environment[self.position[0]][self.position[1]] = '*'           # remove shelf from targets,
                    self.complete = self.check_complete()                           # check if order list is complete.
                else:                                                               # If no target is identified,
                    random_dir = self.random_direction(move_options)                # get pseudo-random direction,
                    self.move(random_dir, environment)                              # move to that direction.
            self.finish_episode()

    def move(self, direction, environment):                                         # Accepts a step (direction)
        self.position += self.moves[direction]                                      # Add step to robot position
        if environment[self.position[0]][self.position[1]] in self.orders:          # Assess score from new position
            self.score += 3
        else:
            self.score -= 1
        self.current_path.append(list(self.position))                               # Store new position

    def random_direction(self, move_options):
        direction_options = []                                                      # Start with no options
        safe_options = []                                                           # and no safe options
        curr_path = self.current_path                                               # Get Current Path
        for proposed_dir in move_options:                                           # For a given direction,
            proposed_pos = self.position + self.moves[proposed_dir]                 # get the resultant position.
            if 0 <= proposed_pos[0] <= 5 and 0 <= proposed_pos[1] <= 5:             # If that is a valid position,
                safe_options.append(proposed_dir)                                   # add it to safe options,
                indicator = True
                for element in curr_path:                                           # Of the visited cells,
                    if all(element == proposed_pos):                                # if the proposed move is not new,
                        indicator = False                                           # it is a visited cell.
                if indicator:                                                       # If it is unvisited,
                    direction_options.append(proposed_dir)                          # add it to the options too
        if bool(direction_options):                                                 # If there are unvisited cells,
            return random.choice(direction_options)                                 # move to one of them.
        else:                                                                       # If all cells have been visited,
            return random.choice(safe_options)                                      # move to a random valid position

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
        if self.protocol == 'path':                                                 # For path protocol:
            for item in self.orders:                                                # If a required item from the
                if item in self.surroundings.values() and item not in self.items:   # order list is adjacent,
                    self.retrieve(item, environment)                                # Retrieve it
            if 'fake' in self.surroundings:                                         # Same process for fake but is
                self.retrieve('fake', environment)                                  # handled in retrieve method
        elif self.protocol == 'random':
            for direction, value in self.surroundings.items():                      # For random protocol:
                if not self.adjacent:                                               # If a target has not been found,
                    if value == 'fake':                                             # If there is a false positive
                        self.surroundings[direction] = wh.fake_shelf(self.warehouse)    # Generate a fake shelf
                    for item in self.orders:                                        # Otherwise, check for targets
                        if item == value and item not in self.items:                # If there is a valid target
                            self.adjacent = True                                    # Change indicator to True,
                            self.next_dir = direction                               # Choose that target,
                            break                                                   # and stop looking

    def retrieve(self, item, environment):
        for direction, shelf in self.surroundings.items():                          # From surroundings,
            if shelf == item:                                                       # find shelf containing target
                if item != 'fake':                                                  # For real items,
                    self.move(direction, environment)                               # move to shelf,
                    self.items.append(item)                                         # grab item,
                    environment[self.position[0]][self.position[1]] = '*'           # do not reward future visits,
                    if self.check_complete():                                       # check if orders completed,
                        self.finish_episode()                                       # finish episode if completed
                    else:
                        back = project_utils.direction_flip(direction)              # if orders remain, move back
                        self.move(back, environment)
                else:
                    fake_shelf = wh.fake_shelf(self.warehouse)
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
                self.worst_path = self.current_path
        self.complete = True
