import random
import numpy as np


def order_gen():
    orders = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']                     # Possible orders
    random.shuffle(orders)                                                          # Shuffle order of orders
    order_set = [orders[x] for x in range(random.randint(1, 10))]                   # Random orders (1-10 in total)
    return order_set


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
