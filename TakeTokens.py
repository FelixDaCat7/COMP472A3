#!/usr/bin/python

import sys
import getopt
import numpy as np
import time
from AlphaBeta import alpha_beta

def main(argv):
    """
    Parse command-line input and compute the best move for the current player using Alpha-Beta pruning algorithm.\n
    Return Move, Value, Number of Nodes Visited, Number of Nodes Evaluated, Max Depth Reached, Avg Effective Branching Factor
    """

    try:
        # simulate help display
        opts, _ = getopt.getopt(argv,"h", ["help"])
        for opt, _ in opts:
            if opt == '-h' or opt == '--help':
                print('usage: TakeTokens.py [-h] [Tokens] [Taken] N [N ...] [Depth]\n\n'
                      'Compute the best move for the current player using Alpha-Beta pruning algorithm\n'
                      'to play a two-player game called PNT: pick numbered-tokens\n\n'
                      'positional arguments:\n'
                      'Tokens       Total number of tokens in the game\n'
                      'Taken        Number of tokens that have already been taken in previous moves\n'
                      '             If this number is 0, this is the first move in a game, which will be played by Max.\n'
                      'N            Sequence of integers indicating the indexes of the already taken tokens,\n'
                      '             ordered from first to last token taken. If N is 0, this list will be empty.\n'
                      'Depth        Search depth. If depth is 0, search to end game states \n'
                      '             (i.e., states where a winner is determined).')
                return
        
        # parse params
        tokens = int(argv[0])
        taken_tokens = int(argv[1])
        if taken_tokens:
            lst_taken_token = list(map(int, argv[2:-1]))
        else:
            lst_taken_token = []
        depth = int(argv[-1])

    except:
        print('usage: TakeTokens.py [-h] [Tokens] [Taken_tokens] N [N ...] [Depth]')
        print('TakenTokens.py: error: invalid format')
        sys.exit(2)

    # create root node
    node = [i for i in range(1 , tokens + 1)]
    for e in lst_taken_token:
        node.remove(e)

    # check last move existence
    last_move = None
    if taken_tokens:
        last_move = lst_taken_token[-1]
    if not depth:
        depth = np.inf

    return alpha_beta(node, depth, -np.inf, np.inf, taken_tokens % 2 == 0, last_move)


if __name__ == "__main__":
    start_time = time.time()
    # print(main(sys.argv[1:]))
    print(main(['3','0','0']))
    execution_time = (time.time() - start_time)
    print("--- %s seconds ---" % execution_time + '\n')