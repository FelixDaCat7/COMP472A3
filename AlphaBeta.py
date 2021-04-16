import numpy as np

class AlphaBeta:
    def __init__(self, node, depth, a, b, isMax, last_move):
        self.best_move = 0
        self.n_visited = 0   # num visited nodes
        self.n_evaluated = 0 # num visited nodes
        self.max_depth = 0   # max depth reached
        self.v = self.alpha_beta(node,       # node
                                 depth,      # depth
                                 -np.inf,    # a
                                 np.inf,     # b
                                 isMax,      # maximizingPlayer
                                 last_move,  # last move
                                 0)          # max depth

    def alpha_beta(self, node, depth, a, b, maximizingPlayer, last_move, max_depth):
        self.n_visited += 1
        if depth == 0 or is_end_game(last_move, node):
            self.n_evaluated += 1
            if self.max_depth < max_depth:
                self.max_depth = max_depth
            return static_board_evaluation(last_move, node, maximizingPlayer)
        if maximizingPlayer:
            v = -np.inf
            children = gen_children(node, last_move)
            for c_move, c_node in children.items():
                child_v = self.alpha_beta(c_node, depth - 1, a, b, False, c_move, 
                                          max_depth + 1)
                v = max(v, child_v)
                a = max(a, v)
                if b <= a:
                    break # b cut-off
            return v
        else:
            v = np.inf
            children = gen_children(node, last_move)
            for c_move, c_node in children.items():
                child_v = self.alpha_beta(c_node, depth - 1, a, b, True, c_move, 
                                          max_depth + 1)
                v = min(v, child_v)
                b = min(b, v)
                if b <= a:
                    break # a cut-off
            return v

def gen_children(node, last_move) -> dict():
    """
    Generate all possible children for node
    """
    children = dict()
    if last_move is None:
        for e in node:
            if  e < -(len(node) // -2) and e % 2 == 1:
                c_node = node.copy()
                c_node.remove(e)
                children[e] = c_node
    else:
        for e in node:
            if (e % last_move == 0) or (last_move % e == 0):
                c_node = node.copy()
                c_node.remove(e)
                children[e] = c_node
    return children

# last_move: integer
# remaining_tokens: set of integers
# is_max_turn: boolean, max turn (true), min turn (false)

# print(static_board_evaluation(5, [3, 2, 6, 8, 10, 11], True))
def static_board_evaluation(last_move, remaining_tokens, is_max_turn) -> float:
    if is_end_game(last_move, remaining_tokens):
        return -1 if is_max_turn else 1
    else:
        evaluation = get_evaluation(last_move, remaining_tokens)
        return evaluation if is_max_turn else -evaluation


def is_end_game(last_move, remaining_tokens) -> bool:
    if last_move is None:
        for e in remaining_tokens:
            if  e < -(len(remaining_tokens) // -2) and e % 2 == 1:
                return False
    else:
        for token in remaining_tokens:
            if last_move % token == 0 or token % last_move == 0:
                return False
    return True


def is_prime(possibly_prime) -> bool:
    is_prime_number = True
    for integer in range(2, possibly_prime):
        if possibly_prime % integer == 0:
            is_prime_number = False
            break
    return is_prime_number


def get_evaluation(last_move, remaining_tokens) -> float:
    # case 1: 1 is still in remaining tokens
    if remaining_tokens[0] == 1:
        return 0
    # case 2: 1 is the last move
    if last_move == 1:
        children = gen_children(remaining_tokens, last_move)
        if len(children) % 2 != 0:
            return 0.5
        else:
            return -0.5
    # case 3: last move is prime
    if is_prime(last_move):
        multiple_count = 0
        for token in remaining_tokens:
            if token % last_move == 0:
                multiple_count = multiple_count + 1
        if multiple_count % 2 != 0:
            return 0.7
        else:
            return -0.7
    # case 4: last move is composite
    prime_divider = 0
    for integer in range(2, last_move):
        if last_move % integer == 0:
            if is_prime(integer):
                prime_divider = integer
    multiples_count = 0
    for integer in remaining_tokens:
        if integer % prime_divider == 0:
            multiples_count = multiples_count + 1
    if multiples_count % 2 != 0:
        return 0.6
    else:
        return -0.6
