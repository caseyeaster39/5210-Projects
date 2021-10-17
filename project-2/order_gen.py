# ORDER GENERATION
import random


def random_alpha():
    letters = ['A',
              'B',
              'C',
              'D',
              'E',
              'F',
              'G',
              'H',
              'I',
              'J',
              'K',
              'L',
              'M',
              'N',
              'O']
    return random.sample(letters, 1)


class Order:
    shelves = random.sample(range(1, 63), random.randint(1, 3))
    div = random_alpha()
