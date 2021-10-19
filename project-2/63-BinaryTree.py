# NODE CREATION
class Node:
    def __init__(self, data):
        self.left_child = None
        self.right_child = None
        self.data = data


i = 1
while i <= 63 // 2:
    child_nodes = []
    parent_nodes = []
    root = Node(i)
    root.left_child = root.data * 2
    root.right_child = (root.data * 2) + 1
    parent_nodes.append(root.data)
    child_nodes.extend([root.left_child, root.right_child])
    i += 1

    print("Parent Shelf: " + str(parent_nodes) + "\t Child Shelves: " + str(child_nodes))
