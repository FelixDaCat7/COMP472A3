import numpy as np
import Heuristic as heuristic

def gen_children(node, last_move) -> dict():
    """
    Generate all possible children for node
    """
    children = dict()
    for e in node:
        if (e % last_move == 0) or (last_move % e == 0):
            new_node = node.copy()
            new_node.remove(e)
            children[e] = new_node
    return children


def alphabeta(node, depth, a, b, maximizingPlayer, last_move):
    """
    Alpha-Beta Pruning Algorithm based on slides
    """
    if depth == 0 or heuristic.is_end_game(last_move, node):
        return heuristic.static_board_evaluation(last_move, node, maximizingPlayer)
    if maximizingPlayer:
        v = -np.inf
        children = gen_children(node, last_move)
        for new_move, new_node in children.items():
            v = max(v, alphabeta(new_node, depth - 1, a, b, False, new_move))
            a = max(a, v)
            if b <= a:
                break # b cut-off
        return v
    else:
        v = np.inf
        children = gen_children(node, last_move)
        for new_move, new_node in children.items():
            v = min(v, alphabeta(new_node, depth - 1, a, b, True, new_move))
            a = min(a, v)
            if b <= a:
                break # b cut-off
        return v


