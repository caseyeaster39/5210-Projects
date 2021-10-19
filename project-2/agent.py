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
        self.cumulative_score = 0
        self.num_runs = 0
        self.step_count = 0
        self.cumulative_steps = 0
        self.max_path = float('-inf')
        self.min_path = float('inf')

    def protocol(self, rand=True, shelves=None, div=None, single_run=False):
        self.order = Order(rand, shelves, div)
        self.wh_search(self.order.div, single_run)
        self.div_search(self.order.shelves, single_run)
        if single_run:
            print("Returning to Warehouse")
            print(f'Final Score: \t{self.score}')
            print(f'Final Step Count: {self.score}')
            self.score = 0
            self.step_count = 0
        else:
            self.scoring_func()

    def wh_search(self, target_node, single_run):
        target_path = path_merge(self.location['warehouse'], target_node)
        self.move(target_path, loc='warehouse', single_run=single_run)

    def div_search(self, shelves, single_run):
        agent_path = path_trace(self.location['div'])

        targets = self.id_search(shelves)
        target_paths = path_forger(targets, agent_path)

        while len(target_paths) > 0:
            this_path = target_paths[0]
            self.move(this_path, loc='div', single_run=single_run)
            agent_path = path_trace(self.location['div'])
            del targets[f'{this_path[-1]}']
            target_paths = path_forger(targets, agent_path)
        self.go_home(single_run)

    def move(self, path, loc, single_run):
        current_tree = self.wh.node_list if loc == 'warehouse' else self.div.node_list
        for step in path:
            self.step_count += 1
            current_node = current_tree[self.location[loc] - 1]
            if step == self.location[loc]:
                continue
            self.location[loc] = step
            if loc == 'div':
                self.score += 1
            else:
                next_node = self.wh.node_list[step - 1]
                self.score_calc(current_node, next_node)
            if single_run:
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

    def go_home(self, single_run):
        self.move(
            path_trace(self.location['div'], reverse=False),
            loc='div', single_run=single_run
        )

    def scoring_func(self):
        self.num_runs += 1
        self.cumulative_score += self.score
        self.cumulative_steps += self.step_count
        average_score = (self.cumulative_score + self.score) / self.num_runs

        average_steps = (self.cumulative_steps + self.step_count) / self.num_runs
        self.max_path = self.step_count if self.max_path < self.step_count else self.max_path
        self.min_path = self.step_count if self.min_path > self.step_count else self.min_path

        print('##########################################')
        print(f'Score this run: \t{self.score}')
        print(f'Average Score: \t\t{round(average_score, 2)}\n')

        print(f'Avg. Step Count: \t{round(average_steps, 2)}')
        print(f'Max Step Count: \t{self.max_path}')
        print(f'Min Step Count: \t{self.min_path}')
        print('##########################################')

        self.score = 0
        self.step_count = 0
