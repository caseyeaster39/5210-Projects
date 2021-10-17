# ORDER GENERATION
import random
from drawtree import draw_level_order

def random_alpha():
    letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
    return letter[random.randint(0, 15)]


def order_func():
    num_items = random.randint(1, 3)
    shelf = random.sample(range(1, 63), num_items)
    order_func.div = random_alpha()
    print('Num of items: ' + str(num_items))
    print('Division: ' + order_func.div)
    print('Shelf Location(s): ' + str(shelf))


def inner_tree_func():
    shelf_list = list(range(1, 64))
    sentence = list(map(str, shelf_list))
    formatted_sent = '{' + ','.join(sentence) + '}'
    draw_level_order(formatted_sent)

order_func()

print('\033[4mShelf tree:\033[0m')

order_func.div = inner_tree_func()

