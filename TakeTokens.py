#!/usr/bin/python

import sys
import getopt
import numpy as np
import time
from AlphaBeta import *

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

    # perform alphabeta
    a = AlphaBeta(tokens, taken_tokens, lst_taken_token, depth)
    return a.output()

if __name__ == "__main__":
    main(sys.argv[1:])
    # main(['3', '0', '0'])
    # main(['7', '1', '1', '2'])
    # main(['10','3','4', '2', '6', '4'])