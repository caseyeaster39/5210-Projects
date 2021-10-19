from project_utils import path_trace, path_merge, path_forger
from warehouse import Warehouse, Division, Order


class Agent:
    def __init__(self):                                                             # Agent initialization
        # Warehouse Components
        self.order = None
        self.location = {
            'warehouse': 1,
            'div': 1
        }
        self.wh = Warehouse()
        self.div = Division()

        # Scoring and Tracking
        self.score = 0
        self.cumulative_score = 0
        self.num_runs = 0
        self.step_count = 0
        self.cumulative_steps = 0
        self.max_path = float('-inf')
        self.min_path = float('inf')

    def protocol(self, rand=True, shelves=None, div=None, single_run=False):    # Main protocol
        self.order = Order(rand, shelves, div)                                  # Generate the order for this run
        self.wh_search(self.order.div, single_run)                              # Search the warehouse for the division
        self.div_search(self.order.shelves, single_run)                         # Enter division and search for order
        if single_run:
            print("Returning to Warehouse")                                     # Printouts for single run
            print(f'Final Score: \t{self.score}')
            print(f'Final Step Count: {self.score}')
            self.score = 0
            self.step_count = 0
        else:                                                                   # Printouts for consecutive runs
            self.scoring_func()

    def wh_search(self, target_node, single_run):                               # Finding the division in warehouse:
        target_path = path_merge(self.location['warehouse'], target_node)       # Merge path agent to target
        self.move(target_path, loc='warehouse', single_run=single_run)          # Move on the merged path

    def div_search(self, shelves, single_run):                                  # Finding shelves in a division:
        agent_path = path_trace(self.location['div'])                           # Trace agent back to root

        targets = self.id_search(shelves)                                       # Iterative Deepening Search -> Nodes
        target_paths = path_forger(targets, agent_path)                         # Create priority queue

        while len(target_paths) > 0:                                            # Until targets have all been retrieved
            this_path = target_paths[0]                                         # Get shortest path
            self.move(this_path, loc='div', single_run=single_run)              # and move there
            agent_path = path_trace(self.location['div'])                       # Get agent path to assess next target
            del targets[f'{this_path[-1]}']                                     # Delete this target from targets
            target_paths = path_forger(targets, agent_path)                     # Recalculate paths to targets
        self.go_home(single_run)                                                # Return to division root

    def move(self, path, loc, single_run):                                      # Move along a path
        current_tree = self.wh.node_list if loc == 'warehouse' \
            else self.div.node_list                                             # Define current tree
        for step in path:
            current_node = current_tree[self.location[loc] - 1]                 # Get current node
            if step == self.location[loc]:
                continue                                                        # Don't step if already there
            self.step_count += 1                                                # Step counter
            self.location[loc] = step                                           # Move agent
            if loc == 'div':
                self.score += 1                                                 # Division weights = 1
            else:
                next_node = self.wh.node_list[step - 1]                         # Get next node
                self.score_calc(current_node, next_node)                        # Score weight for moving along edge
            if single_run:                                                      # Printouts for individual runs
                print(f'Moved to {self.location[loc]} in {loc}, current score: {self.score}')

    def score_calc(self, node1, node2):
        parent_node = node1 if node2.parent == node1.num else node2             # Figure out which node is parent
        child_node = node1 if parent_node != node1 else node2                   # Other node is child

        edge = parent_node.left if parent_node.left[0] == child_node.num \
            else parent_node.right                                              # Retrieve edge weight

        self.score += edge[1]                                                   # Add edge weight to score

    def id_search(self, targets):                                               # Iterative Deepening Search
        results = {}
        for target in targets:                                                  # Loop through current targets
            results[f'{target}'] = 'None'                                       # No initial result
            depth = 0
            while depth <= self.div.max_depth:                                  # Incrementing depth limit for DLS
                result = self.dl_search(target, depth)                          # Try DLS at current depth limit
                if result:
                    results[f'{target}'] = result                               # If target is found, add to results
                    break                                                       # and break out of DLS loop
                depth += 1                                                      # Otherwise, increment depth
        return results

    def dl_search(self, target, depth_limit):
        frontier = list()                                                       # Empty frontier
        frontier.append(self.div.node_list[0])                                  # Start at root
        while len(frontier) > 0:                                                # Until frontier is exhausted
            node = frontier.pop()                                               # Pop top node
            if node.num == target:
                return node                                                     # Return node if target found
            if not node.depth > depth_limit:                                    # If within depth limit
                self.expand(frontier, node)                                     # expand frontier from node
        return None                                                             # If you make it this far, search failed

    def expand(self, frontier, node):
        right_index = node.right[0] - 1                                         # Get frontier node indices
        left_index = node.left[0] - 1

        frontier.append(self.div.node_list[right_index])                        # Add nodes to frontier
        frontier.append(self.div.node_list[left_index])

    def go_home(self, single_run):
        self.move(                                                              # Move back to division root
            path_trace(self.location['div'], reverse=False),
            loc='div', single_run=single_run
        )

    def scoring_func(self):
        # Score calculations
        self.num_runs += 1
        self.cumulative_score += self.score
        average_score = (self.cumulative_score + self.score) / self.num_runs

        # Step calculations
        self.cumulative_steps += self.step_count
        average_steps = (self.cumulative_steps + self.step_count) / self.num_runs
        self.max_path = self.step_count if self.max_path < self.step_count else self.max_path
        self.min_path = self.step_count if self.min_path > self.step_count else self.min_path

        # Report printout
        print(f'Run number {self.num_runs}:')
        print('##########################################')
        print(f'Score this run: \t{self.score}')
        print(f'Average Score: \t\t{round(average_score, 2)}\n')

        print(f'Avg. Step Count: \t{round(average_steps)}')
        print(f'Max Step Count: \t{self.max_path}')
        print(f'Min Step Count: \t{self.min_path}')
        print('##########################################')

        # Reset non-cumulative metrics
        self.score = 0
        self.step_count = 0
