from project_utils import path_trace, path_merge, path_forger
from warehouse import Warehouse, Division, Order


class Agent:
    def __init__(self):
        self.order = None
        self.location = {
            'warehouse': 1,
            'div': 1
        }
        self.wh = Warehouse()
        self.div = Division()

        # Scoring
        self.score = 0
        self.num_runs = 0
        self.cumulative_score = 0
        self.average_score = 0
        self.max_score = 0
        self.min_score = float('inf')

    def protocol(self, rand=True, shelves=None, div=None, printouts=False):
        self.order = Order(rand, shelves, div)
        self.wh_search(self.order.div, printouts)
        self.div_search(self.order.shelves, printouts)
        if printouts:
            print("Returning to Warehouse")
            print(f'Final Score: {self.score}')
        else:
            self.scoring_func()

    def wh_search(self, target_node, printouts):
        target_path = path_merge(self.location['warehouse'], target_node)
        self.move(target_path, loc='warehouse', printouts=printouts)

    def div_search(self, shelves, printouts):
        agent_path = path_trace(self.location['div'])

        targets = self.id_search(shelves)
        target_paths = path_forger(targets, agent_path)

        while len(target_paths) > 0:
            this_path = target_paths[0]
            self.move(this_path, loc='div', printouts=printouts)
            agent_path = path_trace(self.location['div'])
            del targets[f'{this_path[-1]}']
            target_paths = path_forger(targets, agent_path)
        self.go_home(printouts)

    def move(self, path, loc, printouts):
        current_tree = self.wh.node_list if loc == 'warehouse' else self.div.node_list
        for step in path:
            current_node = current_tree[self.location[loc] - 1]
            if step == self.location[loc]:
                continue
            self.location[loc] = step
            if loc == 'div':
                self.score += 1
            else:
                next_node = self.wh.node_list[step - 1]
                self.score_calc(current_node, next_node)
            if printouts:
                print(f'Moved to {self.location[loc]} in {loc}, current score: {self.score}')

    def score_calc(self, node1, node2):
        parent_node = node1 if node2.parent == node1.num else node2
        child_node = node1 if parent_node != node1 else node2

        edge = parent_node.left if parent_node.left[0] == child_node.num else parent_node.right

        self.score += edge[1]

    def id_search(self, targets):
        results = {}
        for target in targets:
            results[f'{target}'] = 'None'
            depth = 0
            while depth <= self.div.max_depth:
                result = self.dl_search(target, depth)
                if result:
                    results[f'{target}'] = result
                    break
                depth += 1
        return results

    def dl_search(self, target, cursive_l):
        frontier = list()
        frontier.append(self.div.node_list[0])
        while len(frontier) > 0:
            node = frontier.pop()
            if node.num == target:
                return node
            if not node.depth > cursive_l:
                self.expand(frontier, node)
        return None

    def expand(self, frontier, node):
        right_index = node.right[0] - 1
        left_index = node.left[0] - 1

        frontier.append(self.div.node_list[right_index])
        frontier.append(self.div.node_list[left_index])

    def go_home(self, printouts):
        self.move(path_trace(self.location['div'], reverse=False), loc='div', printouts=printouts)

    def scoring_func(self):
        self.num_runs += 1
        self.cumulative_score += self.score
        self.max_score = self.score if self.max_score < self.score else self.max_score
        self.min_score = self.score if self.min_score > self.score else self.min_score
        self.average_score = (self.cumulative_score + self.score) / self.num_runs

        print('##########################################')
        print(f'Score this run: \t{self.score}\n')
        print(f'Average Score: \t\t{self.average_score}')
        print(f'Cumulative Score: \t{self.cumulative_score}')
        print(f'Max Score: \t\t\t{self.max_score}')
        print(f'Min Score: \t\t\t{self.min_score}')
        print('##########################################')

        self.score = 0
