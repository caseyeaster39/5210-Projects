class Agent:
    def __init__(self, is_max):
        self.is_max = is_max
        self.value_init = float('-inf') if is_max else float('inf')
        self.sign = 'x' if is_max else 'o'

    def search(self, game, state, alpha, beta, last_action=None):
        player = game.players['max'] if self.is_max else game.players['min']
        other_player = game.players['min'] if self.is_max else game.players['max']

        is_won, utility = game.utility(state)
        if game.free_slots(state) == 0 or is_won:
            return utility, last_action
        value = player.value_init
        move = None
        for action in game.actions(state):
            result = game.result(state, action, player.sign)
            value2, action2 = other_player.search(game, result, alpha, beta, last_action=action)
            if player.value_check(value, value2):
                value, move = value2, action
                alpha, beta = player.update_target(value, alpha, beta)
            if player.check_limit(value, alpha, beta):
                return value, move
        return value, move


class MaxAgent(Agent):
    @staticmethod
    def update_target(value, alpha, beta):
        alpha = max(alpha, value)
        return alpha, beta

    @staticmethod
    def value_check(val, val2):
        return val2 > val

    @staticmethod
    def check_limit(value, alpha, beta):
        return value >= beta


class MinAgent(Agent):
    @staticmethod
    def update_target(value, alpha, beta):
        beta = min(beta, value)
        return alpha, beta

    @staticmethod
    def value_check(val, val2):
        return val2 < val

    @staticmethod
    def check_limit(value, alpha, beta):
        return value <= alpha


class Game:
    def __init__(self, state, max_turn):
        self.state = state
        self.has_ended = False
        self.winner = None

        self.players = {
            'max': MaxAgent(is_max=True),
            'min': MinAgent(is_max=False)
        }
        self.max_turn = max_turn

        self.win_states = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),    # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),    # Columns
            (0, 4, 8), (2, 4, 6)                # Diagonals
        ]

    @classmethod
    def new_game(cls, max_starts=True):
        return cls(state='---------', max_turn=max_starts)

    def auto_game(self):
        while not self.has_ended:
            self.do_turn()

    def turn_input(self, move):
        self.end_turn(move, 'o')

    def do_turn(self):
        player = self.players['max'] if self.max_turn else self.players['min']
        value, move = player.search(self, self.state, float('-inf'), float('inf'))
        self.end_turn(move, player.sign)
        return move

    def end_turn(self, move, sign):
        self.state = self.result(self.state, move, sign)
        self.check_end_game()
        self.max_turn = not self.max_turn

    def utility(self, state):
        for win_condition in self.win_states:
            set_ = set([state[i] for i in win_condition])
            if len(set_) == 1 and '-' not in set_:
                return True, 1 if 'x' in set_ else -1
        return False, 0

    def check_end_game(self):
        state = self.state
        utility = self.utility(state)

        if utility == (True, 1):
            self.winner = type(self.players['max']).__name__
            self.has_ended = True
        elif utility == (True, -1):
            self.winner = type(self.players['min']).__name__
            self.has_ended = True
        elif utility == (False, 0) and self.free_slots(state) == 0:
            self.has_ended = True

    @staticmethod
    def result(state, action, sign):
        if action is None:
            return state
        return state[:action] + sign + state[action+1:]

    @staticmethod
    def actions(state):
        return [i for i in range(len(state)) if state[i] == '-']

    @staticmethod
    def free_slots(state):
        return len([letter for letter in state if letter == '-'])
