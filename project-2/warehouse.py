# WAREHOUSE MAIN FLOOR
class Node:
    def __init__(self, num, is_parent, left=None, right=None):
        self.name = chr(ord('@') + num)
        if is_parent:
            self.left = left
            self.right = right
        self.parent = num // 2 if num > 1 else None


def floor_gen():
    node_list = list()

    node_list.append(Node(1, is_parent=True, left=(2, 20), right=(3, 20)))
    node_list.append(Node(2, is_parent=True, left=(4, 20), right=(5, 30)))
    node_list.append(Node(3, is_parent=True, left=(6, 40), right=(7, 10)))
    node_list.append(Node(4, is_parent=True, left=(8, 10), right=(9, 20)))
    node_list.append(Node(5, is_parent=True, left=(10, 30), right=(11, 20)))
    node_list.append(Node(6, is_parent=True, left=(12, 30), right=(13, 20)))
    node_list.append(Node(7, is_parent=True, left=(14, 20), right=(15, 20)))
    node_list.append(Node(8, is_parent=False))
    node_list.append(Node(9, is_parent=False))
    node_list.append(Node(10, is_parent=False))
    node_list.append(Node(11, is_parent=False))
    node_list.append(Node(13, is_parent=False))
    node_list.append(Node(14, is_parent=False))
    node_list.append(Node(15, is_parent=False))

    return node_list


class Warehouse:
    def __init__(self):
        self.node_list = floor_gen()
