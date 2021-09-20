import random
import numpy as np


def order_gen():
    orders = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']                     # Possible orders
    random.shuffle(orders)                                                          # Shuffle order of orders
    order_set = [orders[x] for x in range(random.randint(1, 10))]                   # Random orders (1-10 in total)
    return order_set


def map_initialize(warehouse):
    if warehouse == 'a':
        coord_dict = {
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
    else:
        coord_dict = {
            'A': [2, 0],
            'B': [2, 1],
            'C': [0, 3],
            'D': [0, 1],
            'E': [0, 2],
            'F': [2, 2],
            'G': [0, 4],
            'H': [2, 3],
            'I': [0, 5],
            'J': [2, 4],
            'K': [4, 2],
            # 'L': [],
            'M': [4, 1],
            'N': [4, 5],
            'O': [5, 3],
            'P': [4, 0],
            'Q': [5, 4],
        }
    empty_arr = np.array([['*' for i in range(6)] for j in range(6)])

    # Each time loop runs "letter is different key from dict.
    for letter, (x_pos, y_pos) in coord_dict.items():    # "letter" represents key of dictionary.
        empty_arr[y_pos][x_pos] = letter                # Key Value ("letter") is placed into empty_arr using x and y

    return empty_arr


def fake_shelf(warehouse):
    if warehouse == 'a':
        return random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'])
    else:
        return random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                              'J', 'K', 'L', 'M', 'N, O', 'P', 'Q'])
