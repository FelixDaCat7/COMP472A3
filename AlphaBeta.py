import numpy as np

class State:
    __slots__ = ('node', 'depth', 'isMax', 'last_move')

    def __init__(self, node, depth, isMax, last_move):
        self.node = node
        self.depth = depth
        self.isMax = isMax
        self.last_move = last_move

class AlphaBeta:
    def __init__(self, tokens, taken_tokens, lst_taken_token, depth):
        """
        Initialize the Alpha-beta pruning algorithm after parsing user input
        """
        # create root node
        node = [i for i in range(1 , tokens + 1)]
        for e in lst_taken_token:
            node.remove(e)
        # determine the existence of a last move
        last_move = None
        if taken_tokens:
            last_move = lst_taken_token[-1]
        # determine the current player
        isMax = taken_tokens % 2 == 0

        self.root = State(node, 0, isMax, last_move)   # root state
        self.depth_limit = depth if depth else np.inf  # depth limit
        self.root_children = dict() # stores direct children of root {state: v} 
        self.n_arrow = 0 # keep count of number of generated children
        self.n_non_leaf = 0 # keep count of number of generated non-leaf children
        # Output variables
        self.best_move = 0  # best move for current player
        self.n_visited = 0  # num visited states
        self.n_eval    = 0  # num visited states
        self.max_depth = 0  # max depth reached

        if isMax: 
            self.v = self.max_value(self.root, -np.inf, np.inf)
        else:
            self.v = self.min_value(self.root, -np.inf, np.inf)

        # select smaller numbered token as best move
        for child, child_v in self.root_children.items():
            if child_v == self.v:
                self.best_move = child.last_move
                break
        # avg effective branching factor
        self.factor = self.n_arrow / self.n_non_leaf


    def max_value(self, state, a, b) -> float:
        """
        Return utility value for MAX
        """
        self.n_visited += 1
        if self.terminal_test(state):
            self.n_eval += 1
            if self.max_depth < state.depth: # update max depth traversed
                self.max_depth = state.depth
            return static_board_evaluation(state) # compute utility value
        v = -np.inf
        self.n_non_leaf += 1
        children = gen_children(state)
        for child in children:
            self.n_arrow += 1
            child_v = self.min_value(child, a, b) # go to MIN child state
            v = max(v, child_v)
            a = max(a, v)
            if child.depth == 1:
                self.root_children[child] = child_v
            if b <= a:
                break # b cut-off
        return v
    
    def min_value(self, state, a, b) -> float:
        """
        Return utility value for MIN
        """
        self.n_visited += 1
        if self.terminal_test(state):
            self.n_eval += 1
            if self.max_depth < state.depth: # update max depth traversed
                self.max_depth = state.depth
            return static_board_evaluation(state) # compute utility value
        v = np.inf
        self.n_non_leaf += 1
        children = gen_children(state)
        for child in children:
            self.n_arrow += 1
            child_v = self.max_value(child, a, b) # go to MAX child state
            v = min(v, child_v)
            b = min(b, v)
            if child.depth == 1:
                self.root_children[child] = child_v
            if b <= a:
                break # b cut-off
        return v

    def terminal_test(self, state) -> bool:
        """
        Return true if state has reached depth limit or is an end state
        """
        return state.depth == self.depth_limit or is_end_game(state)

    def output(self):
        print(f'Move: {self.best_move}\n'
              f'Value: {self.v:.1f}\n'
              f'Number of Nodes Visited: {self.n_visited}\n'
              f'Number of Nodes Evaluated: {self.n_eval}\n'
              f'Max Depth Reached: {self.max_depth}\n'
              f'Avg Effective Branching Factor: {self.factor:.1f}\n')
        return self.best_move, self.v, self.n_visited, self.n_eval, self.max_depth, self.factor

def gen_children(state) -> list():
    """
    Generate all possible children for state
    """
    children = list()
    if state.last_move is None:
        for e in state.node:
            if  e < -(len(state.node) // -2) and e % 2 == 1:
                c_node = state.node.copy()
                c_node.remove(e)
                children.append(State(c_node, state.depth + 1, not state.isMax, e))
    else:
        for e in state.node:
            if (e % state.last_move == 0) or (state.last_move % e == 0):
                c_node = state.node.copy()
                c_node.remove(e)
                children.append(State(c_node, state.depth + 1, not state.isMax, e))
    return children

def static_board_evaluation(state) -> float:
    if is_end_game(state):
        return -1 if state.isMax else 1
    else:
        evaluation = get_evaluation(state)
        return evaluation if state.isMax else -evaluation


def is_end_game(state) -> bool:
    if state.last_move is None:
        for e in state.node:
            if  e < -(len(state.node) // -2) and e % 2 == 1:
                return False
    else:
        for token in state.node:
            if state.last_move % token == 0 or token % state.last_move == 0:
                return False
    return True


def is_prime(possibly_prime) -> bool:
    is_prime_number = True
    for integer in range(2, possibly_prime):
        if possibly_prime % integer == 0:
            is_prime_number = False
            break
    return is_prime_number


def get_evaluation(state) -> float:
    # case 1: 1 is still in remaining tokens
    if state.node[0] == 1:
        return 0
    # case 2: 1 is the last move
    if state.last_move == 1:
        children = gen_children(state)
        if len(children) % 2 != 0:
            return 0.5
        else:
            return -0.5
    # case 3: last move is prime
    if is_prime(state.last_move):
        multiple_count = 0
        for token in state.node:
            if token % state.last_move == 0:
                multiple_count = multiple_count + 1
        if multiple_count % 2 != 0:
            return 0.7
        else:
            return -0.7
    # case 4: last move is composite
    prime_divider = 0
    for integer in range(2, state.last_move):
        if state.last_move % integer == 0:
            if is_prime(integer):
                prime_divider = integer
    multiples_count = 0
    for integer in state.node:
        if integer % prime_divider == 0:
            multiples_count = multiples_count + 1
    if multiples_count % 2 != 0:
        return 0.6
    else:
        return -0.6
